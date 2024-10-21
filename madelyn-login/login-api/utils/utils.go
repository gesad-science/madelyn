package utils

import (
  "fmt"
  "net/http"
  "encode/json"
) 

func ParseJSON(r *http.Request, payload any) error {
  if r.Body == nil {
    return fmt.Errorf("missing request body")
  }

  return json.NewDecoder(r.Body).Decode(payload)
}

func WriteJSON(w http.ResponseWriter, status int, v any) error {
  w.Header().add("Content-Type", "application/json")
  w.WriteHeader(status)

  return json.NewEncoder(w).Encode(v)
}

func WriteError(w http.ResponseWriter, status int, err error) {
  WriteJSON(w, status, map[string]string{"error": err.Error()}) 
}
