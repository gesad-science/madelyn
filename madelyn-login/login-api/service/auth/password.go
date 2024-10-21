package auth

import "golang.org/x/crypto/bcrypt"


func HashPassword(password string) (string, error) {
  hash, err := bcrypt.GenerateFromPassword([]byte(password), bcrypt.DefaultCost)
  if err != nil {
    return "", nil
  }

  return string(hash), nil
}
