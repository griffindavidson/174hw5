Note: I have a homebrew formulae installed called jq which prettifies the JSON output seen below, omit the '| jq' if you don't have it installed for testing
	also as seen, python likes to alphabetically sort the Row entries, so they are all mixed to what their headers should be

GET /companies:

curl -s https://griffindavidson.dev/companies | jq
{
  "Mainline": {
    "Table": {
      "Header": {
        "Data": [
          "Parent Company",
          "Subsidiary Portfolio / Services",
          "HQ / Info",
          "Annual Revenue ($ million)",
          "HomePage",
          "Logo"
        ]
      },
      "Row": [
        {
          "Company": "UPS",
          "HomePage": "https://www.ups.com/",
          "Hubs": {
            "Hub": [
              "55 Glenlake Parkway, Sandy Springs, Georgia, U.S.",
              "UPS is a global leader in logistics, offering a broad range of solutions including the transportation of packages and freight; the facilitation of international trade, and the deployment of advanced technology to more efficiently manage the world of business."
            ]
          },
          "Logo": "ups.jpg",
          "Revenue": "$24,752",
          "Services": "UPS Ground, UPS Freight"
        },
        {
          "Company": "FedEx",
          "HomePage": "https://www.fedex.com",
          "Hubs": {
            "Hub": [
              "942 South Shady Grove Road[1], Memphis, Tennessee, U.S.",
              "FedEx Corporation is an American multinational courier delivery services company headquartered in Memphis, Tennessee. The name FedEx is a syllabic abbreviation of the name of the company's original air division, Federal Express (now FedEx Express), which was used from 1973 until 2000. The company is known for its overnight shipping service, but also for pioneering a system that could track packages and provide real-time updates on package location."
            ]
          },
          "Logo": "fedex.jpg",
          "Revenue": "$14,149",
          "Services": "FedEx Ground, FedEx Freight, FedEx Custom Critical"
        },
        {
          "Company": "J.B. Hunt Transport Services",
          "HomePage": "https://www.jbhunt.com/",
          "Hubs": {
            "Hub": [
              "Lowell, Arkansas",
              "Since 1961, J.B. Hunt Transport Services, Inc., has been a leader in the trucking industry. Hunt Transport was among the first companies to adopt the container trucking approach, in which containers went directly from ships and trains onto trucks."
            ]
          },
          "Logo": "jbhunt.png",
          "Revenue": "$4,527",
          "Services": "Truckload, Dedicated Contract Services, Integrated Capacity Solutions, Intermodal"
        },
        {
          "Company": "YRC Worldwide",
          "HomePage": "https://www.yrcw.com/",
          "Hubs": {
            "Hub": [
              "Overland Park, Kansas, USA",
              "YRC Freight traces its origins to Yellow Transit Company, a bus and taxi company in Oklahoma City in 1924. Yellow Transit later merged with Roadway, the dominant trucking company in the U.S. for decades, and Reimer Express, the leading trucking company in Canada, to form Yellow Roadway Corporation, shortened to YRC Freight. "
            ]
          },
          "Logo": "yrcw.png",
          "Revenue": "$4,869",
          "Services": "YRC Freight, YRC Regional"
        },
        {
          "Company": "Con-way",
          "HomePage": "http://www.con-way.com",
          "Hubs": {
            "Hub": [
              "Ann Arbor Charter Township, Michigan",
              "Con-Way started out in 1929 as Consolidated Truck Lines, a small regional trucking company, in Portland, Oregon. Today, the company operates from more than 400 transportation centers across North America, as well as in 20 countries across five continents. "
            ]
          },
          "Logo": "con-way.png",
          "Revenue": "$3,729",
          "Services": "Con-way Freight, Con-way Truckload"
        },
        {
          "Company": "Swift Transportation",
          "HomePage": "http://www.swifttrans.com/",
          "Hubs": {
            "Hub": [
              "Phoenix, Arizona, United States",
              "In 1966, the company now known as Swift Transportation started out hauling steel from Los Angeles to Arizona and cotton from Arizona back to Southern California. More than four decades later, the company now owns 11 other trucking subsidiaries, operates more than 16,000 trucks and hauls truckload-sized freight all over the U.S., Canada and Mexico. "
            ]
          },
          "Logo": "swift.png",
          "Revenue": "$3,334",
          "Services": "Truckload, Dedicated, Intermodal"
        },
        {
          "Company": "Amazon",
          "HomePage": "https://www.amazon.com",
          "Hubs": {
            "Hub": [
              "123 Amazon Way, Seattle, Washington, U.S.",
              "Amazon is the largest digital retailer in the word"
            ]
          },
          "Logo": "amazon.jpg",
          "Revenue": "$294,291",
          "Services": "Amazon Prime, Amazon Prime Video"
        }
      ]
    }
  }
}

GET /companies/<some company>

curl -s https://griffindavidson.dev/companies/UPS | jq             
{
  "Mainline": {
    "Table": {
      "Header": {
        "Data": [
          "Parent Company",
          "Subsidiary Portfolio / Services",
          "HQ / Info",
          "Annual Revenue ($ million)",
          "HomePage",
          "Logo"
        ]
      },
      "Row": [
        {
          "Company": "UPS",
          "HomePage": "https://www.ups.com/",
          "Hubs": {
            "Hub": [
              "55 Glenlake Parkway, Sandy Springs, Georgia, U.S.",
              "UPS is a global leader in logistics, offering a broad range of solutions including the transportation of packages and freight; the facilitation of international trade, and the deployment of advanced technology to more efficiently manage the world of business."
            ]
          },
          "Logo": "ups.jpg",
          "Revenue": "$24,752",
          "Services": "UPS Ground, UPS Freight"
        }
      ]
    }
  }
}

POST /companies

curl -s -X POST https://griffindavidson.dev/companies \      -H "Content-Type: application/json" \      -d '{"Company": "New Truck Co", "Services": "", "Hubs": {"Hub": []}, "Revenue": "", "HomePage": "", "Logo": ""}' | jq
{
  "success": "Data Successfully added"
}

PUT /companies/<some company>

curl -s -X PUT https://griffindavidson.dev/companies/New%20Truck%20Co \      -H "Content-Type: application/json" \      -d '{"Revenue": "$26,000"}' | jq 
{
  "success": "Successfully updated New Truck Co"
}

POST / PUT proof:

curl -s https://griffindavidson.dev/companies/New%20Truck%20Co | jq                                                                                     
{
  "Mainline": {
    "Table": {
      "Header": {
        "Data": [
          "Parent Company",
          "Subsidiary Portfolio / Services",
          "HQ / Info",
          "Annual Revenue ($ million)",
          "HomePage",
          "Logo"
        ]
      },
      "Row": [
        {
          "Company": "New Truck Co",
          "HomePage": "",
          "Hubs": {
            "Hub": []
          },
          "Logo": "",
          "Revenue": "$26,000",
          "Services": ""
        }
      ]
    }
  }
}

DELETE /companies/<some company>

curl -s -X DELETE https://griffindavidson.dev/companies/New%20Truck%20Co | jq
{
  "success": "Successfully deleted New Truck Co"
}

Error: attempting to GET non-existent company (after deleting New Truck Co)

curl -s https://griffindavidson.dev/companies/New%20Truck%20Co | jq          
{
  "error": "Company not found"
}

Error: attempting to POST existing company

curl -s -X POST https://griffindavidson.dev/companies \      -H "Content-Type: application/json" \      -d '{"Company": "FedEx", "Services": "", "Hubs": {"Hub": []}, "Revenue": "", "HomePage": "", "Logo": ""}' | jq
{
  "error": "Company already exists"
}

Error: attempting to POST without a company name (name is required)

curl -s -X POST https://griffindavidson.dev/companies \      -H "Content-Type: application/json" \      -d '{"Company": "", "Services": "", "Hubs": {"Hub": []}, "Revenue": "", "HomePage": "", "Logo": ""}' | jq 
{
  "error": "Company Name required"
}

Error: attempting to PUT without specifiying a company

curl -s -X PUT https://griffindavidson.dev/companies/New%20Truck%20Co | jq
{
  "error": "Company not found"
}

Error: attempting to delete non-existent company

curl -s -X DELETE https://griffindavidson.dev/companies/Apple | jq           
{
  "error": "Company not found"
}
