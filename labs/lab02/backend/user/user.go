package user

import (
	"context"
	"errors"
	"regexp"
	"sync"
	"strings"
)

// User represents a chat user

type User struct {
	Name  string
	Email string
	ID    string
	// You could add more fields such as CreatedAt, Status, etc.
}

// Validate checks if the user data is valid
func (u *User) Validate() error {
	if strings.TrimSpace(u.Name) == "" {
		return errors.New("name is required")
	}
	if strings.TrimSpace(u.ID) == "" {
		return errors.New("id is required")
	}
	if !isValidEmail(u.Email) {
		return errors.New("invalid email")
	}
	return nil
}

// isValidEmail checks if an email address has a simple valid format
func isValidEmail(email string) bool {
	// This is a simple regex for demonstration, not fully RFC compliant
	re := regexp.MustCompile(`^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$`)
	return re.MatchString(email)
}

// UserManager manages users

type UserManager struct {
	ctx   context.Context
	users map[string]User // userID -> User
	mutex sync.RWMutex    // Protects users map
	// No extra fields needed for now
}

// NewUserManager creates a new UserManager
func NewUserManager() *UserManager {
	return &UserManager{
		ctx:   context.Background(),
		users: make(map[string]User),
	}
}

// NewUserManagerWithContext creates a new UserManager with context
func NewUserManagerWithContext(ctx context.Context) *UserManager {
	return &UserManager{
		ctx:   ctx,
		users: make(map[string]User),
	}
}

// AddUser adds a user
func (m *UserManager) AddUser(u User) error {
	if m.ctx != nil {
		select {
		case <-m.ctx.Done():
			return errors.New("context cancelled")
		default:
		}
	}
	if err := u.Validate(); err != nil {
		return err
	}
	m.mutex.Lock()
	defer m.mutex.Unlock()
	if _, exists := m.users[u.ID]; exists {
		return errors.New("user already exists")
	}
	m.users[u.ID] = u
	return nil
}

// RemoveUser removes a user
func (m *UserManager) RemoveUser(id string) error {
	m.mutex.Lock()
	defer m.mutex.Unlock()
	if _, exists := m.users[id]; !exists {
		return errors.New("user not found")
	}
	delete(m.users, id)
	return nil
}

// GetUser retrieves a user by id
func (m *UserManager) GetUser(id string) (User, error) {
	m.mutex.RLock()
	defer m.mutex.RUnlock()
	user, exists := m.users[id]
	if !exists {
		return User{}, errors.New("not found")
	}
	return user, nil
}
