<br />
<h1 align="center">ZETTEL MERKEN</h1>
<p align="center">Supercharge your learning by combining two of the most revolutionary ideas in knowledge enhancement!</p>
<br />

# Introduction

Zettel stands for "note" and Merken stands for "remember" in German. A literal translation would imply "Remember your notes", but that is an overly simplistic definition of what the title stands for.

To be precise, Zettel-merken is a fusion of two impactful ideas in the field of knowledge management and learning enhancement: "Zettelkasten" and "Spaced Repetition".

## What is Zettelkasten?

The [Wikipedia article](https://en.wikipedia.org/wiki/Zettelkasten) defines zettelkasten as "The zettelkasten is a system of note-taking and personal knowledge management used in research and study".

[zettelkasten.de](https://zettelkasten.de/introduction/) is a wonderful little site that is all about, well, zettelkasten. Do read the [introduction](https://zettelkasten.de/introduction/). To pick an excerpt from there:

> A Zettelkasten is a personal tool for thinking and writing. [...] The difference to other systems is that you create a web of thoughts instead of notes of arbitrary size and form, and emphasize connection, not a collection.

If I had to explain the concept to someone in a hurry, I'd say: Zettelkasten = Mind Map + Flash Cards

Of course, it is _not_ entirely either, so I would recommend following the links above for a more detailed understanding.

### How I use Zettelkasten

I take notes for _everything_! From doing research for my web novels to learning new languages, from my transaction history to ongoing projects, suffice to say I have a _lot_ of notes. However, I have come to realize that not all my notes are highly connected. Rather, a collection of notes is usually extremely cohesive with one another but largely decoupled from the rest. So I follow a sort-of watered-down system like so:

0. One single folder called "notes"
1. An index (No direct notes made here, only links), usually named "index.md".
2. A "hub" for each topic. Imagine a hub as a collection (like a notebook or a drawer). One hub usually points to one large topic.
3. A "zettel" for each atomic piece of info. All zettels for a topic are linked into the hub and are stored in a folder usually named after the same.

That's it! To expand on the above, here is a sample of my current notes directory:

```sh

~/notes
├── index.md
├── books-and-articles.md
├── books-and-articles
│  ├── atomic-habits.md
│  └── ledger-accounting.md
├── code-notes.md
├── code-notes
│  ├── python.md
│  ├── python
│  │  └── basics.md
│  ├── vim.md
├── learning-french.md
├── learning-french
│  ├── basics-1.1.md
│  ├── basics-1.2.md
│  ├── basics-1.3.md
├── transactions.md
├── transactions
│  ├── 01-2022.md
│  └── 02-2022.md
├── zettel-merken.md
└── zettel-merken
   └── research-in-spaced-repeatition.md

```

As you can see above, I have hubs after each topic: zettel-merken, books-and-articles, learning-french, etc. Each hub has a file.md and folder with the same name. I take all my notes in neovim in markdown format (No special plugins!). I have written a couple of helper functions that make it easy to create hubs and zettels but that is all.

Concerning zettels, I try to have them in an easily digestible format. Each zettels has a microscopic focus on the information it is trying to convey. That is: all the content inside a zettel must directly relate to a single matter or flow in one direction. The size of the file is irrelevant, although I try to keep it short and simple.

Also, I _try_ to avoid more than one layer of nesting below the "notes" folder but in some cases like the above "python" notes, it is inevitable. However, there should never be a need to go beyond two layers.

After following the above system consistently for a few months, you'll have a decent-sized collection of notes all linked together and also in a proper structure. That being said, simply "collecting" notes is never going to help you learn in the long term. That is where the Spaced Repetition comes in!

## TODO

## What is Spaced Repetition?

### How I use Spaced Repetition

## Setting up Zettel-Merken

## Advanced Configuration

## Tips and tools

## Notes & Bugs
