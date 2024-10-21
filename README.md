# madelyn

## LIM
### This API allows users to tailor LLM responses to the rules and models of their systems and can be easily integrated with other systems via HTTP requests.

### Features

- **Treating attributes** from an user message in [NLP].
- **Treating the entity** 
- **Treating the intent**
---

### Documentation

#### URL Base

The URL base for the requisitions is: http://0.0.0.0:8080/treat

### Endpoints

#### 1. **Treating the attributes**
   - **Description:** Receives an wrong attribute value and returns a correction.
   - **Method:** `Post`
   - **Endpoint:** `/attributes`
   - **Example:**

     ```bash
     curl -X Post http://0.0.0.0:8080/treat/attributes
     ```

   - **Answer:**

     ```json
     {
       "key" : "name",
       "value" : "pedro",
       "processed_atts" : {},
       "model_name" : "mistral",
       "user_input" : "add student with name pedro",
       "current_entity" : "student",
       "current_intent" : "create"
     }
     ```