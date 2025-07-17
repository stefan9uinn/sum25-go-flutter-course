import 'package:flutter/material.dart';
import 'chat_service.dart';
import 'dart:async';

// ChatScreen displays the chat UI
class ChatScreen extends StatefulWidget {
  final ChatService chatService;
  const ChatScreen({super.key, required this.chatService});

  @override
  State<ChatScreen> createState() => _ChatScreenState();
}

class _ChatScreenState extends State<ChatScreen> {
  // Text controller for input
  final TextEditingController _controller = TextEditingController();

  // State for messages, loading, and error
  List<String> _messages = [];
  bool _loading = true;
  String? _error;
  StreamSubscription<String>? _subscription;

  @override
  void initState() {
    super.initState();
    _connectAndSubscribe();
  }

  void _connectAndSubscribe() async {
    setState(() {
      _loading = true;
      _error = null;
    });
    try {
      await widget.chatService.connect();
      _subscription = widget.chatService.messageStream.listen((msg) {
        setState(() {
          _messages.add(msg);
        });
      }, onError: (err) {
        setState(() {
          _error = err.toString();
        });
      });
      setState(() {
        _loading = false;
      });
    } catch (e) {
      setState(() {
        _error = e.toString();
        _loading = false;
      });
    }
  }

  @override
  void dispose() {
    _controller.dispose();
    _subscription?.cancel();
    super.dispose();
  }

  void _sendMessage() async {
    final text = _controller.text.trim();
    if (text.isEmpty) return;
    try {
      await widget.chatService.sendMessage(text);
      _controller.clear();
    } catch (e) {
      setState(() {
        _error = e.toString();
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_loading) {
      return const Center(child: CircularProgressIndicator());
    }
    if (_error != null) {
      return Center(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Text('Error: $_error', style: const TextStyle(color: Colors.red)),
            const SizedBox(height: 12),
            ElevatedButton(
              onPressed: _connectAndSubscribe,
              child: const Text('Retry'),
            ),
          ],
        ),
      );
    }
    return Scaffold(
      appBar: AppBar(title: const Text('Chat')),
      body: Column(
        children: [
          Expanded(
            child: ListView.builder(
              reverse: false,
              itemCount: _messages.length,
              itemBuilder: (context, idx) {
                return ListTile(
                  title: Text(_messages[idx]),
                );
              },
            ),
          ),
          const Divider(height: 1),
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 8.0, vertical: 10),
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _controller,
                    decoration: const InputDecoration(
                      hintText: 'Enter message...',
                    ),
                    onSubmitted: (_) => _sendMessage(),
                  ),
                ),
                IconButton(
                  icon: const Icon(Icons.send),
                  onPressed: _sendMessage,
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
