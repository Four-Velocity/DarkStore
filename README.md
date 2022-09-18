[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=for-the-badge&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Powered by: DigitalOcean](https://img.shields.io/badge/Powered%20By-Digital%20Ocean-0168FF?style=for-the-badge&labelColor=ffffff&logo=digitalocean)](https://darkstore.four-velocity.com)

# Darkstore Crypto API

This is a small test task that emulates crypto portfolio

## How to run project locally

1. Copy .env.example file  
   `cp .env.example .env`
2. Replace `FINNHUB_SECRET` variable in .env file with real [finnhub](https://finnhub.io/) API key
3. Run project
   `docker-compose up --build`
4. The backend will be available on [http://127.0.0.1:8080](http://127.0.0.1:8080)

## How to test project

You have to options:

1. You can [run project locally](#how-to-test-project) with docker-compose and it will be available
   on [http://127.0.0.1:8080](http://127.0.0.1:8080)
2. You can use deployed demo: [https://darkstore.four-velocity.com](https://darkstore.four-velocity.com)

In both cases here is the requirements :point_down:

* You can find the swagger docs on the root endpoint
* You can send requests directly from swagger
* __Send POST request on `/populate` endpoint to fill db with dummy values and users__ (no AUTH needed)
* Two users will be created: _admin_ and _John Doe_
* For all other endpoints you have to authenticate with JWT token. You can get them
  from [https://jwt.io/](https://jwt.io/) or copy from the [tokens](#tokens) section below.
    * If you will use jwt.io pls ensure that the algorithm is __HS256__ and the `"name"` field value is `"admin"`
      or `"John Doe"`
* With _admin_ user you can clean db by sending POST request to `/wipe` endpoint. If you perform that action all users
  and portfolios will be deleted. You can always populate new data with `/populate` endpoint, but your previous changes
  won't be saved

### Tokens

#### John Doe

`eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c`

#### admin

`eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6ImFkbWluIiwiaWF0IjoxNTE2MjM5MDIyfQ.T26Dm4buOBRdxNs58srk1l_N5y1Dxii9y-YMj-9J7mM`

