# Query.Select

## Inspiration

We got the idea of this project when jokingly a member suggested to make "a program to look a large dataset of websites and give the best results," this person was saying to create Google. But even though this idea wasn't all that serious and of course we couldn't create google in 24 hours or at all, we started to think if we could spin the idea and create something new and useful. We spent a good amount of time of going back and forth about what it means to make a "new" type of search engine. We settled on the idea of creating a site that allowed the users to search through specific links they knew would have relevant information. They either did not want to comb through the entire page or did not want to find all relating information from the many hyperlinks that so many sites have today. This is where we believe our project comes in.

## What it does

After receiving the links the user wants to search through and the query they are specifically asking about, we run a web crawler to parse through the provided links, saving the body of the page and recursively creating new crawlers whenever a hyperlink it touched. We do this so that we do not only look at the pages the user provides, but also look at other relevant sites through the links they have.
Once the crawler has stored the body of the next, they are sent, along with the query, to a word2vec model trained to find the similarity between the text in the query and the text from the website. I will get more into how we use this model in the "How we built it."
Once we have the data from the model, we send it back for processing; this includes forwarding the query and page bodies to WolfRam for a re-ranking of the top finds for increased accuracy and taking the related link and relevant text segments from it and displaying it on our webpage. I will also get into the WolfRam usage more in the next section.
Finally, when everything is displayed, all the relevant information is displayed for the user to enjoy!

## How we built it

Starting with the most intriguing parts of the project, we make use of a trained word2vec table and a network on Wolfram to find the similarities between query and document body. The word2vec table we use is GloVe, which we use for the speed of a lookup table to find results quickly. When looking through the body of the page, we use a sliding window to compare the greatest number of permutations that could result in similar text to the query. 
ELMo is the language model we use from WolfRam. It being trained on a billion words makes it slower then GloVe, but the added benefit is having a context sensitive result. This means that ELMo can distinguish between the word "play" meaning "to play the piano" and "play" when it means "a play from a football game." This is why we use both GloVe and ELMo: one will give the faster results for people who just want a quick search, and while they look through those results, WolfRam will be finding the more accurate ordering of the top candidates.
For the frontend we used React Bootstrap, allowing us to make a simple yet elegant website to display the findings our backend finds, which was written in Python and WolfRam.

## Challenges we ran into

One of the largest challenges was actually getting React to talk with python because it actually lacks the functionality we needed in our project. To get around this we made a server that would wait for the get requests from the server and forward those request into the python process it will spawn. Though this was not our first solution and we had to stop what we were doing to reevaluate the best way to move forward.
We also had challenges with other parts of the project, such as having to learn the language that WolfRam uses for their networks and how to then deploy those networks to the cloud where they can be ran from our python code.

## Accomplishments that we're proud of

Wee am amazed by the sophistication of our project given that we only had 24 hours to do it. We have two fully functional ways of searching the web for results that have semantically related meanings given the context of the sentence it is in. We also have it working with a website to present the data in a way that is digestible and, I mean lets be honest it matters, looks good.
Furthermore, we are also proud, and relieved, that we just got everything to work. We had many times when it looked like integrating different parts of the project seemed near impossible, like when React just wouldn't talk to Python or when we realized we needed to load in an entire model to the cloud and the local machine to run both of them, or when the recursive crawlers would halt at a seemingly random moment.
Overall we are very proud of what we acomplished together.

## What we learned

We learned a bunch of new things: GloVe for the initial semantic analysis, WolfRam and ELMo for a slower but more sophisticated analysis of what GloVe found, as well as their general programming workflows.

## What's next for Query.Select

One thing would be increased speed. We suffer because of the cloud based processing of the WolfRam API, as we have to ask it to make these calls every time we want to reevaluate text. A simple solution to this would be to have it running locally where it could serve clients specifically instead of the server have to be served from WolfRam and then the client from the server. We would also like to perform caching of documentation of well known languages and frameworks, this way we do not have to traverse over these pages multiple times. Finally general cleanup and polish of the project, making more of a website, having a more unified backend, generally the problems that come up when you have a limited time to implement a complex project. We are excited to see where we can take Query.Select!

A [HackRPI](https://hackrpi.com/) Project!
