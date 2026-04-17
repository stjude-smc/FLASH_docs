.. _flash_development_guide-style_guide:

Style Guide
===========

This section describes programming style to help keep the code base consistent and “readable”.

- **Wire diagrams** should fit within one screen to avoid scrolling. To achieve this, avoid unnecessary white space, keep the scope of each VI to one well-defined purpose, and extract code blocks to new helper VI’s where it makes sense. This also helps to minimize chances of merge conflicts in team development.

- **Terminals** should use a consistent 4x2x4 pattern, with inputs on the left and outputs on the right. Avoid wiring in more than 4 inputs – use clusters instead.

- Top left terminal is the primary input and top right is primary output. This is usually an object wire (for class methods) or resource handle (for file access, etc.).


.. figure:: ../_static/flash_development_guide/img_flash_development_guide_0001.png
   :name: fig-flash_development_guide-1
   :alt: img_flash_development_guide_0001.png

- The bottom left should be error in and bottom right error out.

- Middle left terminals are for input parameters.

- Middle right terminals are outputs, such as results of a method call.

- Center terminals are often used for enum inputs because this allows long names to above or below the VI node in the block diagram to save space.

- Center terminals should not be used as outputs.

- **Align** VI nodes ****from left to right **so that the error wire is straight from input to output. This helps keep program flow clear and linear. Use the error wire as the primary means of controlling parallelization within one VI.


.. figure:: ../_static/flash_development_guide/img_flash_development_guide_0002.png
   :name: fig-flash_development_guide-2
   :alt: Keep icons simple, with a top bar to identify the module/class and the middle part giving a brief text description of the function. Avoid custom icon images. An exception are HAL override methods (“hooks”), which include a downward blue arrow.

   Keep icons simple, with a top bar to identify the module/class and the middle part giving a brief text description of the function. Avoid custom icon images. An exception are HAL override methods (“hooks”), which include a downward blue arrow.

- **Comments** on wire diagrams should describe obscure constant values, algorithms, and document assumptions.

- **VI descriptions** should give a one sentence summary of the purpose of the function and describe each input and output terminal.


.. figure:: ../_static/flash_development_guide/img_flash_development_guide_0003.png
   :name: fig-flash_development_guide-3
   :alt: img_flash_development_guide_0003.png

- **Naming:** method names should be verbs, class member names should be nouns, words should be separated by spaces, and each word should be capitalized.

- **Use virtual folders** to organize class methods and set access scope explicitly for each virtual folder. See an example at right. Outside of classes, use auto-populating virtual folders so that the project and disk organization matches.


- Helper VIs, typedefs, and other resources should be owned by the lvlib that uses them and located in the same folder on disk. Use the Resources folder only sharing across modules.

- Use the built-in Actor Framework “Create Message” and “Rescript this message” macros to create and update messages. Do not manually create/modify them.
