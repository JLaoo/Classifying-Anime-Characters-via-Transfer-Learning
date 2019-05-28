Link to original repository: https://github.com/JLaoo/Classifying-Waifus-via-Transfer-Learning

# Classifying the characters of New Game! via Transfer Learning

Based off of Freedomofkeima's blog post found here: https://freedomofkeima.com/blog/posts/flag-15-image-recognition-for-anime-characters

# Steps

1) scrape_images
- Scrapes images from the first 3 pages of search results for the wanted characters via safebooru (not tryna get banned lmao).
- Saves these images in local directories.
2) detect_faces
- Using nagadomi's lbpcascade_animeface (https://github.com/nagadomi/lbpcascade_animeface) we can detect faces and save the cropped results to yet another local directory.
- Some faces aren't able to be detected. Nagadomi has a more accurate face detector released (https://github.com/nagadomi/animeface-2009) but runtime is a lot slower and it's more difficult to implement.
3) resize_cropped
- Resizes all of the images into 96x96 squares. Not sure if this step is actually necessary since TensorFlow resizes images anyways, but I didn't think that far ahead at this step.
- I had to manually clean the resized images after this step since lbpcascade_animeface isn't 100% accurate and some pictures contained multiple faces. I wasn't too careful while cleaning so there might be some inaccurate datapoints and duplicates, but it's probably(?) negligible.
4) split_dataset
- Splits images into training and test sets. My dataset really wasn't that large so most inaccuracies in the model can probably be attributed to the lack of data.
- For each character, I had 85% (rounded down) of their faces as training data and the rest as test data.
5) modeling
- Trained with 20 epochs at first, got 100% accuracy on the training set but only like 60% accuracy on the test set probably due to overfitting. Changed it to 10 epochs and got >90% accuracy on the training set and about 80% accuracy on the test set. This can probably be fine tuned to yield higher accuracy even with the small dataset.
- Again, the lack of data is the biggest limitation at this step, but I'm too lazy to go find more data.

As we can see below, the accuracy for the training set is quite high!
![30 predictions in the training set](https://i.imgur.com/jeq92EF.png)

The accuracy for the test set is not as high, but still respectable!
![30 predictions in the test set](https://i.imgur.com/xBwfcPG.png)

# Remarks
Overall a fun little project that I enjoyed working on. I chose New Game! since it's probably the closest there is to an anime about software engineering. Got familiar with TensorFlow (I had only used SKLearn before this) and also got my first taste of neural nets and image classification.

# To do
- Increase size of dataset.
- Tune hyperparameters.
- Check that the python scripts work (I've only tested the ipynb).

Copyright for all images are owned by their respective creators.

lbpcascade_animeface.xml is created by nagadomi/lbpcascade_animeface.

Heavily influenced by Freedomofkeima (https://github.com/freedomofkeima)
