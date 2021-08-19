

## About The Project

"Lastic" (eraser) is monolithic back-end service that implements app features such as friends, answers sharing and token verification.

### Built With

* [Starlette](https://www.starlette.io/)
* [Pydantic](https://pydantic-docs.helpmanual.io/) 
* [MongoDB](https://www.mongodb.com/) (As a main database)



<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

### Local testing

1. Clone the repo
   ```sh
   git clone https://github.com/paradiary/lastic.git
   ```
2. Install PyPi packages
   ```sh
   pip install -r requirements.txt
   ```
3. Set LASTIC_DEBUG enviroment variable to `true`
    ```sh
    export LASTIC_DEBUG=true
    ```
4. Run uvicorn server
    ```sh
    uvicorn app:app --reload
    ```

### Deployment

1. Make a docker image (specify tag in %tag%)
   ```shell
   docker build -t %tag% ./
   ```
2. Save it 
   ```shell
   docker image save > image
   ```
3. Transfer it to server
4. Load docker image
   ```shell
   docker image load -i image
   ```
5. Create docker container and start it in slient mode
   ```shell
   docker run -dp 80:80 %tag% 
   ```

### OpenAPI schema generation
If you need fresh API schema just run this server in DEBUG mode and make a request to `localhost:8000/schema`

After this you can import it to Postman, or generate MD with [this](https://github.com/Aurora81/openapi2md) tool
