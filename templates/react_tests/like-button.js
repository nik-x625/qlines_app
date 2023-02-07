'use strict';

function LikeButton() {
    const [liked, setLiked] = React.useState(false);

    if (liked) {
        return 'You liked this!';
    }

    return React.createElement(
        'button',
        {
            onClick: () => setLiked(true),
        },
        'Like'
    );
}

document.querySelectorAll('.xclass').forEach((rootNode) => {
    const root = ReactDOM.createRoot(rootNode);
    // Read the comment ID from a data-* attribute.
    const commentID = parseInt(rootNode.dataset.commentid, 10);
    root.render(
        React.createElement(LikeButton, { commentID: commentID })
    );
});
