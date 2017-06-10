# Pyramid OpenId Connect

Experimental implementation of the OpenId Connect (OIDC) protocol using
(pyoidc)[https://github.com/OpenIDC/pyoidc].

## TODO

* Configuration of client, secret and provider URI.

The functionality will provide authentication using the authorization code
flow. This flow has the following steps requiring functionality as noted:

### 1. Client prepares an Authentication Request containing the desired request parameters.

* Trigger this upon request of a view registered with `pyramid.view.forbidden_view_config`.
* Generate the state and nonce and store it in the session.

### 2. Client sends the request to the Authorization Server.

### 3. Authorization Server Authenticates the End-User.
### 4. Authorization Server obtains End-User Consent/Authorization.
### 5. Authorization Server sends the End-User back to the Client with an Authorization Code.
### 6. Client requests a response using the Authorization Code at the Token Endpoint.
### 7. Client receives a response that contains an ID Token and Access Token in the response body.
### 8. Client validates the ID token and retrieves the End-User's Subject Identifier.
