import numpy as np
from sklearn.metrics import confusion_matrix
from sklearn.utils.multiclass import unique_labels
import matplotlib.pyplot as plt


def plot_confusion_matrix(y_true,
                          y_pred,
                          title=None,
                          classes=None,
                          colorbar=True,
                          normalize=False,
                          cmap=plt.cm.Blues):
    """
    Plot confusion matrix.
    :param y_true: list or array
    :param y_pred: list or array
    :param title: figure title
    :param classes: Classes for showing as xy labels. If None, auto use unique classes in the confusion matrix.
    :param colorbar: Show or not show the colorbar.
    :param normalize: Normalize the confusion matrix or not.
    :param cmap: Select cmap.
    :return: cm(ndarray), axes object
    """
    # Set title
    if not title:
        if normalize:
            title = 'Normalized confusion matrix'
        else:
            title = 'Confusion matrix, without normalization'

    # Compute confusion matrix
    cm = confusion_matrix(y_true, y_pred)

    # Normalize
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

    # Plot basic graph
    fig, ax = plt.subplots()
    im = ax.imshow(cm, interpolation='nearest', cmap=cmap)

    # Default classes: use only use the labels that appear in the data
    if classes is None:
        classes = unique_labels(y_true, y_pred)

    # Check if lengths of cm and classes are the same
    if cm.shape[0] != len(classes):
        raise ValueError('Classes length {} is not consistent with confusion matrix side length {}.'.format(
            cm.shape[0],
            len(classes)
        ))

    # Set ax settings
    ax.set(xticks=np.arange(cm.shape[1]),
           yticks=np.arange(cm.shape[0]),
           xticklabels=classes,
           yticklabels=classes,
           title=title,
           ylabel='True label',
           xlabel='Predicted label')

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")

    print(cm)

    # Set color bar
    if colorbar is True:
        ax.figure.colorbar(im, ax=ax)

    # Loop over data dimensions and create text annotations.
    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, format(cm[i, j], fmt),
                    ha="center", va="center",
                    color="white" if cm[i, j] > thresh else "black")

    # Fit plots within figure cleanly
    fig.tight_layout()
    return cm, ax
