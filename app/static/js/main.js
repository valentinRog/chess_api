const get_piece_url = (piece) => {
    let name = piece.toUpperCase();
    if (piece === name) {
        return `${url_for_assets}/w${name}.svg`;
    } else {
        return `${url_for_assets}/b${name}.svg`;
    }
}