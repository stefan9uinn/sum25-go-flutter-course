class UserService {
  Future<Map<String, String>> fetchUser() async {
    // Simulate fetching user data for tests
    await Future.delayed(const Duration(milliseconds: 300));
    return {'name': 'Test User', 'email': 'test@example.com'};
  }
}
