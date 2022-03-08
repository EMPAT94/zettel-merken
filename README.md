<br />
<h1 align="center">ZETTEL MERKEN</h1>
<p align="center">Supercharge your learning by combining two of the most revolutionary ideas in knowledge enhancement!</p>
<br />

# Introduction

Zettel stands for "note" and Merken stands for "remember" in German. A literal translation would imply "Remember your notes", but that is an overly simplistic definition of what the title stands for.

To be precise, Zettel Merken is a fusion of two impactful ideas in the field of knowledge management and learning enhancement: "Zettelkasten" and "Spaced Repetition".

## What is Zettelkasten?

The [Wikipedia article](https://en.wikipedia.org/wiki/Zettelkasten) defines zettelkasten as "The zettelkasten is a system of note-taking and personal knowledge management used in research and study".

<br />
<div align="center">
<a title="David B. Clear, CC BY-SA 4.0 &lt;https://creativecommons.org/licenses/by-sa/4.0&gt;, via Wikimedia Commons" href="https://commons.wikimedia.org/wiki/File:Zettelkasten_paper_schematic.png"><img width="512" alt="Zettelkasten paper schematic" src="https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Zettelkasten_paper_schematic.png/512px-Zettelkasten_paper_schematic.png"></a>
</div>
<br />

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

Thus, my `index.md` will look like:

```markdown
# INDEX

- [Learning French](./learning-french.md)

- [Code Notes](./code-notes.md)

- [Transactions](./transactions.md)
```

and my `learning-french.md` and `transaction.md` respectively:

```markdown
# Learning French

- [Basics 1.1](./learning-french/basics-1.1.md)

- [Basics 1.2](./learning-french/basics-1.2.md)

- [Basics 1.3](./learning-french/basics-1.3.md)
```

```markdown
# Transactions

- [01-2022](./transactions/01-2022.md)

- [02-2022](./transactions/02-2022.md)
```

Concerning zettels, I try to have them in an easily digestible format. Each zettels has a microscopic focus on the information it is trying to convey. That is: all the content inside a zettel must directly relate to a single matter or flow in one direction. The size of the file is irrelevant, although I try to keep it short and simple.

For example, `basics-1.1` might look like:

```markdown
# Basic 1.1

## Level 0

- un = a (sounds: un)

- et = and (sounds: ae)

- un chat = a cat (sounds: un shaa)

- un homme = a man (sounds: un oum)

- un garcon = a boy (sounds: un gars-on)

- un chat et un homme
  - A cat and a man
```

and a transaction file `01-2022` would be:

```markdown
# 01-2022

| Date | From | To  | Amount | Category | Tag | Comment |
| ---- | ---- | --- | ------ | -------- | --- | ------- |
```

Also, I _try_ to avoid more than one layer of nesting below the "notes" folder but in some cases like the above "python" notes, it is inevitable. However, there should never be a need to go beyond two layers.

After following the above system consistently for a few months, you'll have a decent-sized collection of notes all linked together and also in a proper structure. That being said, simply "collecting" notes is never going to help you learn in the long term. That is where the Spaced Repetition comes in!

## What is Spaced Repetition?

Excerpt from [Wikipedia article](https://en.wikipedia.org/wiki/Spaced_repetition):

> The basis for spaced repetition research was laid by Hermann Ebbinghaus, who suggested that information loss over time follows a forgetting curve, but that forgetting could be reset with repetition based on active recall.

<br />
<div align="center">
<a title="The original uploader was Icez at English Wikipedia., Public domain, via Wikimedia Commons" href="https://commons.wikimedia.org/wiki/File:ForgettingCurve.svg"><img width="256" alt="ForgettingCurve" src="https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/ForgettingCurve.svg/256px-ForgettingCurve.svg.png"></a>
</div>
<br />

Excerpt from [e-student.org](https://e-student.org/spaced-repetition/):

> Spaced repetition is a memory technique that involves reviewing and recalling information at optimal spacing intervals until the information is learned at a sufficient level.

### How I use Spaced Repetition

Or rather how I to use Spaced Repetition _using Zettel Merken_. In the code above, you'll notice a `config.example.json` file. It contains path to each of my "hub" in `note_folders` array.

So, for example, if I wished to add my french vocabulary to the learning track as and when I learn new words, I would have the following config:

```json
  "note_folders": [
    {
      "path": "/path/to/notes/learning-french",
    }
  ],
```

Once set, I will automatically get an email for each lesson at specified intervals! Génial!

The current interval spacing is : Day 1 -> Day 3 -> Day 6 -> Day 14 -> Day 30 -> Day 60

## TODO

## Setting up Zettel-Merken

### systemd timer

- Create directoy for systemd in .config

  ```sh
  mkdir -p $HOME/.config/systemd/user
  ```

- Copy unit files into above directory

  ```sh
  cp -v ./job/zettel-merken.service $HOME/.config/systemd/user/zettel-merken.service
  cp -v ./job/zettel-merken.timer $HOME/.config/systemd/user/zettel-merken.timer
  ```

- Reload systemd daemon

  ```sh
  systemctl --user daemon-reload
  ```

- Start timer, autostarts on boot

  ```sh
  systemctl --user enable --now zettel-merken.timer
  ```

- Ensure timer is 'active'

  ```sh
  systemctl --user status zettel-merken.timer
  ```

- Done!

## Advanced Configuration

## Tips and tools

## Roadmap

## Notes & Bugs
