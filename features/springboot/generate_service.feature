Feature: Generate Service For Springboot

  Scenario: Successful Generate
    Given the project name and class object is processed and ready as context
    When the jinja process the context
    Then the service file content is generated
