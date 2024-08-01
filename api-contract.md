# Users

## 1. Film object

```
{
  id: integer
  film_name: string
  cover: string
  author: string
  actors: list
  story: string
  genre: list
  rating: float
  release_date: datetime
  price: integer
}
```



**GET /**
----
  Returns all film in the system.
* **URL Params**  
  None
* **Data Params**  
  None
* **Headers**  
  Content-Type: application/json  
* **Success Response:**  
* **Code:** 200  
  **Content:**  
```
{
  film: [
           {<film_object>},
           {<film_object>},
           ...
           {<film_object>}
         ]
}
```





**GET /film/{id}**
----
  Returns the specified film.
* **URL Params**  
  *Required:* `id=[integer]`
* **Data Params**  
  None
* **Headers**  
  Content-Type: application/json  
  Authorization: Bearer `<OAuth Token>`
* **Success Response:** 
  * **Code:** 200  
  *  **Content:**  `{ <film_object> }` 
* **Error Response:**  
  * **Code:** 404  
  * **Content:** `{ error : "Film doesn't exist" }`  





## 2. Cart
```
{
  id_user: integer
  id_film: integer
  isSelected: boolean
}
```



**GET /cart**
----
  Returns all films added to card by a specified user.
* **URL Params**  
  None
* **Data Params**  
  None
* **Headers**  
  Content-Type: application/json  
  Authorization: Bearer `<OAuth Token>`
* **Success Response:**  
* **Code:** 200  
  **Content:**  
```
{
  cart: [
          { <film_object>: isSeleted },
          { <film_object>: isSeleted },
          { <film_object>: isSeleted }
        ]
}
```
* **Error Response:**  
  * **Code:** 401  
  **Content:** `{ error : "You are unauthorized to make this request." }`


<!-- -------------------------------------------------------------- -->

**POST /cart/{id_film}**
----
  Add a film to cart's user
* **URL Params**  
  *Requires:* `id_film=[integer]`
* **Data Params**  
```
{
  id_user: integer,
  id_film: integer
}
```
* **Headers**  
  Content-Type: application/json  
  Authorization: Bearer `<OAuth Token>`
* **Success Response:**  
* **Code:** 200  
  **Content:**  `{ id_film: <id> }` 
* **Error Response:**  
  * **Code:** 401  
  * **Content:** `{ error : "You are unauthorized to make this request." }`

