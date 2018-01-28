from struct import pack, unpack

from twisted.internet import reactor
from twisted.internet.protocol import Factory
from twisted.internet.protocol import Protocol
from twisted.protocols.basic import LineOnlyReceiver

from app import PersonMsg_pb2


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
                print('length',length)
                # 如果body接收完整
                if len(self._buffer) >= 4 + length:
                    # body部分
                    packet = self._buffer[4:4 + length]
                    # protobuf字节码转成Student对象
                    student = PersonMsg_pb2.Student()
                    student.ParseFromString(packet)

                    # 调用protobufReceived传入Student对象
                    self.protobufReceived(student)
                    # 去掉_buffer中已经处理的消息部分
                    self._buffer = self._buffer[4 + length:]
                else:
                    break;
            else:
                break;

    def protobufReceived(self, student):
        raise NotImplementedError

    def sendProtobuf(self, student):
        # Student对象转为protobuf字节码
        data = student.SerializeToString()
        # 添加Header前缀指定protobuf字节码长度
        self.transport.write(pack(">I", len(data)) + data)

class TcpServerHandle(MyProtocol):

    counter =0;


    def __init__(self,factory):
        self.factory=factory

    # 新的连接建立
    def connectionMade(self):
        self.factory.client.add(self)
        print('connectionMade')

    # 连接断开
    def connectionLost(self, reason):
        self.factory.client.remove(self)
        print('connectionLost')

    # 接收到新数据
    def protobufReceived(self, data):
        self.counter += 1
        print('数量:', str(self.counter))
        print('dataReceived', data)
        # 将接收到的Student输出
        print('ID:' + str(data.id))
        print('Name:' + data.name)
        print('Email:' + data.email)
        print('Friends:')
        for friend in data.friends:
            print(friend)
        for client in self.factory.client:
            if client.id==11:
                client
        # 创建一个Student并发送给客户端
        student2 = PersonMsg_pb2.Student()
        student2.id = 9
        student2.name = '服务器'  # 中文需要转成UTF-8字符串
        student2.email = '123@abc.com'
        student2.friends.append('X')
        student2.friends.append('Y')
        self.sendProtobuf(student2)



class TcpLineServerHandle(LineOnlyReceiver):
    counter =0;
    def connectionMade(self):
        print('connectionMade')

    # 连接断开
    def connectionLost(self, reason):
        print('connectionLost')

    # 接收到新的一行数据
    def lineReceived(self, data):
        self.counter += 1
        print('数量:', str(self.counter))
        print('lineReceived:' + str(data))


class TcpServerFactory(Factory):
    def __init__(self):
        self.clients = set() # set集合用于保存所有连接到服务器的客户端

    def buildProtocol(self, addr):
        return TcpServerHandle(self)

reactor.listenTCP(8080, TcpServerFactory())
reactor.run()
