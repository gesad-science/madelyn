package user

import (
  "net/http"
  "testing"
  "encoding/json"
	
  "github.com/gesad-science/login-api/types"
)

func TestUserServiceHandler(t *testing.T) {
  userStore := &mockUserStore{}
  handler := NewHandler(userStore)

  t.Run("shoud fail if user payload is invalid", func(t *testing.T) {
    payload := types.RegisterUserPayload{
      FirstName: "user",
      LastName: "123",
      Email: "",
      Password: "asd"
    }

    marshlaled, _ := json.Marshal(payload)

    req, err := http.NewRequest(http.MethodPost, "/register", bytes.NewBuffer(marshlaled))
    if err != nil {
      t.Fatal(err)
    }
  })
}

type mockUserStore struct {}

func (m *mockUserStore) GetUserByEmail(email string) (*User, error) {
  return nil, nil
}


func (m *mockUserStore) GetUserByID(id int) (*User, error) {
  return nil, nil
}

func (m *mockUserStore) CreateUser(User) error {
  return nil
}
