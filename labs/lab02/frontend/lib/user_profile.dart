import 'package:flutter/material.dart';
import 'user_service.dart';

// UserProfile displays and updates user info
class UserProfile extends StatefulWidget {
  final UserService userService; // Accepts a user service for fetching user info
  const UserProfile({Key? key, required this.userService}) : super(key: key);

  @override
  State<UserProfile> createState() => _UserProfileState();
}

class _UserProfileState extends State<UserProfile> {
  // State for user data, loading, and error
  Map<String, String>? _userData;
  bool _loading = true;
  String? _error;

  @override
  void initState() {
    super.initState();
    _fetchUser();
  }

  void _fetchUser() async {
    setState(() {
      _loading = true;
      _error = null;
    });
    try {
      final user = await widget.userService.fetchUser();
      setState(() {
        _userData = user;
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
              onPressed: _fetchUser,
              child: const Text('Retry'),
            ),
          ],
        ),
      );
    }
    return Scaffold(
      appBar: AppBar(title: const Text('User Profile')),
      body: _userData == null
        ? const Center(child: Text('No user data found.'))
        : Padding(
            padding: const EdgeInsets.all(24.0),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.start,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const SizedBox(height: 16),
                Text(
                  'Name: ${_userData!['name'] ?? ''}',
                  style: const TextStyle(fontSize: 20),
                ),
                const SizedBox(height: 12),
                Text(
                  'Email: ${_userData!['email'] ?? ''}',
                  style: const TextStyle(fontSize: 18, color: Colors.grey),
                ),
                const SizedBox(height: 24),
                ElevatedButton(
                  onPressed: _fetchUser,
                  child: const Text('Refresh'),
                ),
              ],
            ),
          ),
    );
  }
}
