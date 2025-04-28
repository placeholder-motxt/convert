Feature: Generate ZIP That Contains Springboot project

    Scenario: ZIP Contains model folder and Consists of All Available model
        Given the parsed class diagram project name and group id
        When the zip is unzip
        Then the zip contains model folder that consists of all models

    Scenario: ZIP Contains repository folder for All Available model
        Given the parsed class diagram project name and group id
        When the zip is unzip
        Then the zip contains repository folder for all models

    Scenario: ZIP Contains service folder for All Available model
        Given the parsed class diagram project name and group id
        When the zip is unzip
        Then the zip contains service folder for all models

    Scenario: ZIP Contains controller folder for All Available model
        Given the parsed class diagram project name and group id
        When the zip is unzip
        Then the zip contains controller folder for all models

    Scenario: ZIP Contains Generated application.properties file
        Given the parsed class diagram project name and group id
        When the zip is unzip
        Then the zip contains application.properties

    Scenario: Empty Diagram
        Given the context JSON with no diagram type
        When the content is parsed
        Then program will raise error for no diagram

    Scenario: Invalid Diagram
        Given the context JSON with invalid diagram
        When content is parsed
        Then program will raise error for invalid diagram
