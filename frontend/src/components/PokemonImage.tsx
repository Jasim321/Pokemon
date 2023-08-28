import React, { useState } from 'react';

interface PokemonImageProps {
  imageUrl: string;
  altText: string;
}

const PokemonImage: React.FC<PokemonImageProps> = ({ imageUrl, altText }) => {
  const [imageError, setImageError] = useState(false);

  const handleImageError = () => {
    setImageError(true);
  };

  return imageError ? (
    <div>No Image Available</div>
  ) : (
    <img src={imageUrl} alt={altText} onError={handleImageError} />
  );
};

export default PokemonImage;
