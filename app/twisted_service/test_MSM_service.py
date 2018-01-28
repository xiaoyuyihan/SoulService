from struct import pack, unpack

from twisted.internet import reactor
from twisted.internet.protocol import Factory
from twisted.internet.protocol import Protocol
from twisted.enterprise import adbapi

from app import IMessage_pb2

"""
:type   
"""
TYPE_SYSTEM_VALIDATION = 1

# 初始化连接池
db = adbapi.ConnectionPool('MySQLdb', db='soul_sql', user='root',
                           passwd='3.1415926lijunyi', host='localhost',
                           charset='utf8', cp_max=10)


# 错误信息，输出到SQL

def printError(error):
    print(error)


def delete_message(columnID):
    db.runInteraction(_conditional_delete, columnID).addErrback(printError)


def _conditional_delete(tx, columnID):
    tx.execute("DELETE FROM message_miss WHERE id=" + str(columnID))


def insert_message(message):
    db.runInteraction(_conditional_insert, message)


# 把数据插入到数据库中
def _conditional_insert(tx, message):
    insert_sql = "INSERT INTO message_miss (sendID,acceptID,message,time,type) values %s" \
                 % str((message.sendid, message.toid, message.message, message.time, str(message)))
    tx.execute(insert_sql)


# 编码、解码器 其中Header部分是常规的大字节序（Big-Endian）的4字节整数
# 固定字节数的Header改为小字节序（Little-Endian）的4字节整数。
class MyProtocol(Protocol):
    # 用于暂时存放接收到的数据
    _buffer = b""

    def dataReceived(self, data):
        # 上次未处理的数据加上本次接收到的数据
        self._buffer = self._buffer + data
        # 一直循环直到新的消息没有接收完整
        while True:
            # 如果header接收完整
            if len(self._buffer) >= 4:
                # 按小字节序转int
                length, = unpack(">I", self._buffer[0:4])
                print('length', length)
                # 如果body接收完整
                if len(self._buffer) >= 4 + length:
                    # body部分
                    packet = self._buffer[4:4 + length]
                    # 字节码转成Student对象
                    student = IMessage_pb2.Message()
                    student.ParseFromString(packet)

                    self.sortingType(student)
                    # 去掉_buffer中已经处理的消息部分
                    self._buffer = self._buffer[4 + length:]
                else:
                    break
            else:
                break

    # 根据类型判断是否发送

    def sortingType(self, message):
        raise NotImplementedError

    def sendMessage(self, student):
        # Message对象转为protobuf字节码
        data = student.SerializeToString()
        # 添加Header前缀指定protobuf字节码长度
        self.transport.write(pack(">I", len(data)) + data)
        print('write')

        """
        查询该帐号的离线消息
        """

    def query_message(self, phone):
        query_string = "SELECT * FROM message_miss WHERE acceptID=" + phone + " ORDER BY id ASC"
        db.runQuery(query_string) \
            .addCallback(self.switchThread) \
            .addErrback(printError)

    def switchThread(self, messages):
        reactor.callFromThread(self.createMessage, messages)    # 切换到reactor

    def createMessage(self, messages):
        if messages is not None:
            for message in messages:
                IMessage = IMessage_pb2.Message(sendid=message[1], toid=message[2],
                                               message=message[3],
                                               time=message[4], type=message[5])
                self.sendMessage(IMessage)
                delete_message(message[0])
        else:
            print("No such user")


class TcpServerHandle(MyProtocol):
    id = 0

    def __init__(self, factory):
        self.factory = factory

    # 新的连接建立
    def connectionMade(self):
        print('connectionMade')

    # 连接断开
    def connectionLost(self, reason):
        if self in self.factory.clients:
            self.factory.clients.remove(self)
        print('connectionLost')

    def sortingType(self, message):
        # 注册ID，获取离线消息
        if message.type == TYPE_SYSTEM_VALIDATION:
            self.id = message.sendid
            self.factory.clients.add(self)
            reactor.callInThread(self.query_message, self.id)  # 将耗时的业务逻辑logic(data)放到线程池中运行，deferToThread返回值类型是Deferred
        else:
            self.distributionMessage(message)

    # 分发接收到的新数据
    def distributionMessage(self, message):
        Falg = False
        print(str(message))
        for client in self.factory.clients:
            print('id', client.id)
            print('toid', message.toid)
            if client.id == message.toid:
                print('True')
                Falg = True
                client.sendMessage(message)
        if Falg is False:
            reactor.callInThread(insert_message, message)  # 在线程池中运行logic(data)耗时任务，不在reactor线程中运行


class TcpServerFactory(Factory):
    def __init__(self):
        self.clients = set()  # set集合用于保存所有连接到服务器的客户端

    def buildProtocol(self, addr):
        return TcpServerHandle(self)


reactor.suggestThreadPoolSize(8)

reactor.listenTCP(12345, TcpServerFactory())
reactor.run()
