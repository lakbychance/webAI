Read the article to know more about this project -> https://blog.lakbychance.com/prototyping-a-qa-web-using-openai

Check out `openai` cook book from where the [original code](https://github.com/openai/openai-cookbook/tree/main/solutions/web_crawl_Q%26A) is picked and modified.

### Installation
* Have `python3` installed on your system.
* Run `pip3 install -r requirements.txt`. 
* If you run into `setuptools` related error, then install `setuptools` as well. 

### Running
* Add `OPENAI_API_KEY: <API TOKEN>` to `.env` file.
* `python3 server.py` would start the flask server.

### Usage
Hit the `http://localhost:5000/ask` route with **required** query params of `question` and `url`. 
There is also an optional `recursive` query parameter which is `false` by default to avoid crawling other links within a page. Make it `true` 
to crawl links matching the `url` signature.

Examples :- 
http://localhost:5000/ask?question=What%20are%20the%20latest%20updates%20to%20middleware%20%3F&url=https%3A%2F%2Fnextjs.org%2Fblog&recursive=true
