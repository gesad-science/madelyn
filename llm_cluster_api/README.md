# Documenting API (you can also use swagger if you prefer)

## - Model related endpoints

- GET /models

    > Endpoint that provides the name of all registered models

- GET /models/{model_name}

    > Endpoint that provides more detaild information about a specific promtp

- GET /models/unregistered

    > Endpoint that provides the name of all provided models that arent already registered

- DELETE /models/{model_name}

    > Endpoint that deletes a specified model`s configuration, making it unregistered

- POST /models

    > Endpoint that registers a specified model, that should be listed as unregistered, receiving its configurations within the request body. If the specified model is already registered it returns a bad request and the older configuration persists.


- PUT /models

    > Endpoint that registers a specified model, that should be listed as unregistered, receiving its configurations within the request body. If the specified model is already registered it overwrite the older configuration.

    
- POST /model/{model_name}/query

    > Endpoint that makes a specified model run as query. The query is specified within the request body


## - Prompt related endpoints
- GET /model/{model_name}/prompts

    > Endpoint that provides a list with all prompts of a model

- GET /model{model_name}/prompts/{prompt_uid}

    > Endpoint that provides more specific information about a specific prompt

- DELETE /model{model_name}/prompts/{prompt_uid}

    > Endpoint that deletes a specific prompt template

- POST /model{model_name}/prompts/

    > Endpoint that adds a provided prompt, from body by the way, to the prompt alternatives list of a model

- PUT /model{model_name}/prompts/{prompt_uid}

    > Endpoint that swaps the main prompt of a model with the specified prompt. The prompt needs to be registered as an prompt alternative

- PUT /model{model_name}/prompts/

    > Endpoint that swaps the main prompt of a model with the prompt specified at the request body. It results in the exclusion of the older main prompt



## - Validation related endpoints

- GET /validations

    > Endpoint that provides a list of all possible validations

- GET /models/{model_name}/validations

    > Endpoint that provides a list of all validations registered to a specified model


- DELETE /models/{model_name}/validations/{validation_number}

    > Endpoint that provides erases a specified validation from a also specified model. If it isn't registered, returns bad request

- POST /models/{model_name}/validations/{validation_number}

    > Endpoint that provides adds a specified validation from a also specified model. If it is already registered, returns bad request