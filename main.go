package main

import (
	"encoding/json"
	"log"
	"net/http"
	"reflect"
	"strconv"

	"github.com/gorilla/mux"
)

// Model for Product
type Product struct {
	ID    int    `json:"id"`
	Name  string `json:"name"`
	Desc  string `json:"desc"`
	Price int    `json:"price"`
	Type  string `json:"type"`
}

// Slice of Products
var products []Product

// Get All Product
func getAllProduct(w http.ResponseWriter, r *http.Request) {
	json.NewEncoder(w).Encode(products)
}

// Get Single Product
func getSingleProduct(w http.ResponseWriter, r *http.Request) {
	// Get id parameter from request
	params := mux.Vars(r)
	item_id, _ := strconv.Atoi(params["id"])

	for _, item := range products {
		if item.ID == item_id {
			// Return JSON response of the selected item
			json.NewEncoder(w).Encode(item)
			return
		}
	}

	// Return HTTP status 404 Not Found if product id is not found
	w.WriteHeader(http.StatusNotFound)
}

// Create New Product
func createProduct(w http.ResponseWriter, r *http.Request) {
	// New product item
	var newProduct Product
	err := json.NewDecoder(r.Body).Decode(&newProduct)
	if err != nil {
		// Return HTTP status 400 Bad Request if request body data is not valid
		w.WriteHeader(http.StatusBadRequest)
		json.NewEncoder(w).Encode(map[string]string{"message": "Invalid body data"})
		return
	}

	// Check the next id number from existing products
	next_id := 1
	if reflect.ValueOf(products).IsValid() {
		for _, item := range products {
			if item.ID >= next_id {
				next_id = item.ID + 1
			}
		}
	}

	// Append the new item
	newProduct.ID = next_id
	products = append(products, newProduct)

	// Return empty response body with HTTP status 201 Created
	// and a Location header with URL to read the created item
	scheme := "http"
	if r.TLS != nil {
		scheme = "https"
	}
	locationURL := scheme + "://" + r.Host + r.RequestURI + "/" + strconv.Itoa(next_id)
	w.Header().Add("Location", locationURL)
	w.WriteHeader(http.StatusCreated)
}

// Update A Product
func updateProduct(w http.ResponseWriter, r *http.Request) {
	// Get id parameter from request
	params := mux.Vars(r)
	item_id, _ := strconv.Atoi(params["id"])

	for i, item := range products {
		if item.ID == item_id {
			// New product item
			var newProduct Product
			err := json.NewDecoder(r.Body).Decode(&newProduct)
			if err != nil {
				// Return HTTP status 400 Bad Request if request body data is not valid
				w.WriteHeader(http.StatusBadRequest)
				json.NewEncoder(w).Encode(map[string]string{"message": "Invalid body data"})
				return
			}

			// Remove selected item from slice
			products = append(products[:i], products[i+1:]...)

			// Append new item to slice
			newProduct.ID = item_id
			products = append(products, newProduct)

			// Return empty response body with HTTP status 201 Created
			// and a Location header with URL to read the updated item
			scheme := "http"
			if r.TLS != nil {
				scheme = "https"
			}
			locationURL := scheme + "://" + r.Host + r.RequestURI
			w.Header().Add("Location", locationURL)
			w.WriteHeader(http.StatusCreated)
			return
		}
	}

	// Return HTTP status 404 Not Found if product id is not found
	w.WriteHeader(http.StatusNotFound)
}

// Delete A Product
func deleteProduct(w http.ResponseWriter, r *http.Request) {
	// Get id parameter from request
	params := mux.Vars(r)
	item_id, _ := strconv.Atoi(params["id"])

	for i, item := range products {
		if item.ID == item_id {
			// Remove selected item from slice
			products = append(products[:i], products[i+1:]...)

			// Return HTTP status 204 No Content and empty response body
			w.WriteHeader(http.StatusNoContent)
			return
		}
	}

	// Return HTTP status 404 Not Found if product id is not found
	w.WriteHeader(http.StatusNotFound)
}

// Middleware to log route requests
func routeLogger(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		log.Printf("\033[33m%-7s\033[0m %s\n", r.Method, r.RequestURI)
		next.ServeHTTP(w, r)
	})
}

// Middleware to set header content-type to JSON
func responseJSON(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Add("Content-Type", "application/json")
		next.ServeHTTP(w, r)
	})
}

func main() {
	// Static data
	products = append(products,
		Product{
			ID:    1,
			Name:  "Donut",
			Desc:  "Delicious",
			Price: 5000,
			Type:  "food",
		},
		Product{
			ID:    2,
			Name:  "Croissant",
			Desc:  "Amazing",
			Price: 7000,
			Type:  "food",
		},
	)

	router := mux.NewRouter()
	router.Use(routeLogger)
	router.Use(responseJSON)

	router.HandleFunc("/product", getAllProduct).Methods("GET")
	router.HandleFunc("/product", createProduct).Methods("POST")
	router.HandleFunc("/product/{id}", getSingleProduct).Methods("GET")
	router.HandleFunc("/product/{id}", updateProduct).Methods("PUT")
	router.HandleFunc("/product/{id}", deleteProduct).Methods("DELETE")

	var httpAddress string = "127.0.0.1:5000"
	log.Print("\033[32mSTART\033[0m   listening on http://" + httpAddress)
	log.Fatal(http.ListenAndServe(httpAddress, router))
}
