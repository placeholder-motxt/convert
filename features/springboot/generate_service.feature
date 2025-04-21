Feature: Generate Service For Springboot

  Scenario: Successful Generate CRUD Only
    Given the project name and class object with no method is processed and ready as context
    When the jinja process the context
    Then the service file content is generated for CRUD

  Scenario: Successful Generate CRUD and Class Diagram Method
    Given the project name and class object with method is processed and ready as context
    When the jinja process the context
    Then the service file content is generated for CRUD and method

  Scenario: Succesful Generate Class Diagram Method Only
    Given the project name and private class object with method is processed and ready as context
    When the jinja process the context
    Then the service file content is generated for methods only

  Scenario: Successful Generate Private Class Diagram with No Method
    Given the project name and private class object with no method and ready as context
    When the jinja process the context
    Then the service file content is generated with empty method
