from flask import Flask, request, redirect, Response, render_template

import json
import base64
import requests

response = requests.get("https://api.open-notify.org/this-api-doesnt-exist")
print(response.status_code)
