# Misc. Repository

Here are things that I wanted to be on my github.
Each of these probably don't need their own little repositories.

## a numbers game

A mastermind clone using the cli for a UI.

## hashtagify rank

Calling hashtagify on various words (or many words in a paragraph) to get and rank them by how popular they are.
Put in a blog post, get out suggestions for what to tag it with when you share the post on twitter.

## memcheck

A little tool I made to help explain how memory works to someone.
When talking about bits and bytes, datatypes, and memoy consumption it's hard to visualize this "memory" thing.

memcheck outputs memory locations, strings of bytes as binary, their decimal representation, and if applicable the character associated with that character code.

## test fuzzy matching

A set of functions to test the differences and similarities of various algorithms. Strings are converted into vectors like you'd find here:

https://blog.nishtahir.com/2015/09/20/fuzzy-string-matching-using-cosine-similarity/

Those vectors are then given to the various algorithms. The idea is to evaluate the algorithms to use for fuzzy string matching.

## ama update

Uses PRAW to, periodically, check a given user's recent submissions for an AMA.

For when you can just never seem to catch your favorite person's rare AMA.

## discord notify

Uses the 'rewrite' branch of the discord.py library.
Uses the most recent aiohttp, discord might complain about this, but ignore that warning.

Hosts a small python web server (aiohttp) and, upon a request to localhost on port 8082, will update the discord channel via a webhook.
For example, to have the webhook/bot communicate "Hello World" you would do a GET request to http://localhost:8082/Hello%20World.
