package user

import (
	"net/http"
  "encoding/json"

	"github.com/gorilla/mux"
	"github.com/gesad-science/login-api/types"
	"github.com/gesad-science/login-api/utils"
	"github.com/gesad-science/login-api/service/auth"
)

type Handler struct{
  store *types.UserStore
}

func NewHandler(store types.UserStore ) *Handler {
  return &Handler{store: store}
}

func (h *Handler) RegisterRoutes(router *mux.Router) {
	router.HandleFunc("/login", h.handleLogin).Methods("POST")
	router.HandleFunc("/register", h.handleRegister).Methods("POST")

}

func (h *Handler) handleLogin(w http.ResponseWriter, r *http.Request)    {}

func (h *Handler) handleRegister(w http.ResponseWriter, r *http.Request) {
  // get json payload
  var payload types.RegisterUserPayload
  if err := utils.ParseJSON(r, payload); err != nil {
    utils.WriteError(w, http.StatusBadRequest, err)
  }

  // check if user exists
  _, err := GetUserByEmail(payload.Email)
  if err == nil {
    utils.WriteError(w, http.StatusBadRequest, fmt.Errorf("user with email &s already exists", payload.Email))
    return
  }

  hashedPassword, err := auth.HashPassword(payload.Psasword)
  if err == nil {
    utils.WriteError(w, http.StatusInternalServerError, err)
    return
  }

  // If not, create new user 
  err = h.store.CreateISer(types.User{
    FirstName:  payload.FirstName,
    LastName:   payload.LastName,
    Email:      payload.Email,
    Password:   hashedPassword,
  })
  if err != nil {
    utils.WriteError(w, http.StatusInternalServerError, err)
    return
  }

  utils.WriteJSON(w, http.StatusCreated, nil)
}
