import 'dart:async';

// ChatService handles chat logic and backend communication
class ChatService {
  // Use a StreamController to simulate incoming messages for tests
  final StreamController<String> _controller =
      StreamController<String>.broadcast();

  // Add simulation flags for connection and send failures
  bool failSend = false;
  bool failConnect = false;

  ChatService();

  Future<void> connect() async {
    // Simulate connection (for tests)
    if (failConnect) {
      await Future.delayed(const Duration(milliseconds: 200));
      throw Exception('Connection failed (simulated)');
    }
    await Future.delayed(const Duration(milliseconds: 200));
    // Could add a "connected" flag here if needed
  }

  Future<void> sendMessage(String msg) async {
    // Simulate sending a message (for tests)
    await Future.delayed(const Duration(milliseconds: 100));
    if (failSend) {
      throw Exception('Send failed (simulated)');
    }
    _controller.add(msg);
  }

  Stream<String> get messageStream {
    // Return stream of incoming messages (for tests)
    return _controller.stream;
  }

  void dispose() {
    _controller.close();
  }
}
