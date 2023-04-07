<br />

<h2 align="center">

[Rompt.ai](https://rompt.ai) Python Library

</h2>

<br />

Rompt streamlines your workflow, improves collaboration, enhances GPT model performance, and provides seamless integration with its CLI tool and output format support.


Features
--------

*   Version control and changelog on prompts
*   Generate prompts from template strings
*   Pull prompts from Rompt into your codebase


Installation
------------

Install the client & CLI library:

```bash
pip install rompt
```

Pull your prompts into your codebase using the CLI:

```bash
rompt pull --token {YOUR_TOKEN}
```


Usage
-----

To use the library, you'll first need to import it:

```py
from rompt import generate

generated_with_metadata = generate(
  prompt_name="your-prompt-name",
  template_object={
    NAME: "Michael",
    DIRECTION: "Generate a Tweet"
  },
)

prompt = generated_with_metadata.get('prompt')
# Your result is now in the prompt variable
```


Track History
-------------

```py
from rompt import generate, track

# ...continued from above

track(generated_with_metadata)

# Your GPT responses can be included; example with OpenAI:

const gpt_response = openai.Completion.create({
  prompt=prompt,
  #...
})

track(generated_with_metadata, gpt_response)
```


Documentation
-------------

For detailed documentation, including API references and more examples, please visit the [the Rompt.ai website](https://rompt.ai/docs).


Contributing
------------

We welcome contributions to the Rompt Node.js library. If you'd like to contribute, please submit a pull request on GitHub.


License
-------

This project is licensed under the MIT License. For more information, please see the [LICENSE](https://github.com/your_github_username/rompt-/blob/main/LICENSE) file.