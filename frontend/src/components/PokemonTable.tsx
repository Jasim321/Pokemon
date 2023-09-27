import React, { ChangeEvent, useEffect, useState } from 'react';
import axios from 'axios';
import Pagination from 'react-bootstrap/Pagination';
import FormControl from 'react-bootstrap/FormControl';
import Table from 'react-bootstrap/Table';
import PokemonImage from './PokemonImage';

interface Pokemon {
    id: number;
    name: string;
    base_experience: number;
    height: number;
    weight: number;
    image_url: string;
}

const ITEMS_PER_PAGE = 10;

const PokemonTable: React.FC = () => {
    const [pokemonData, setPokemonData] = useState<Pokemon[]>([]);
    const [currentPage, setCurrentPage] = useState(1);
    const [searchTerm, setSearchTerm] = useState('');
    const [filterBy, setFilterBy] = useState('');

    const fetchPokemonData = async () => {
        try {
            const requestConfig = {
                params: { page: currentPage, name: searchTerm },
            };
            const response = await axios.get(`/pokemons`, requestConfig);
            setPokemonData(response.data.items);
        } catch (error) {
            console.error('Error fetching Pokémon data:', error);
        }
    };

    useEffect(() => {
        fetchPokemonData();
    }, [currentPage, searchTerm, filterBy]);

    const handlePageChange = (page: number) => {
        setCurrentPage(page);
    };

    const handleSearchChange = (event: ChangeEvent<HTMLInputElement>) => {
        setSearchTerm(event.target.value);
        setCurrentPage(1);
    };

    const handleFilterChange = (event: ChangeEvent<any>) => {
        const newFilter = event.target.value;
        setFilterBy(newFilter);
        setCurrentPage(1);
    };

    // Determine the maximum values
    const maxExperience = Math.max(...pokemonData.map(pokemon => pokemon.base_experience));
    const maxHeight = Math.max(...pokemonData.map(pokemon => pokemon.height));
    const maxWeight = Math.max(...pokemonData.map(pokemon => pokemon.weight));

    const filteredPokemonData = pokemonData
        .filter((pokemon) => {
            const nameMatch = searchTerm ? pokemon.name.toLowerCase().includes(searchTerm.toLowerCase()) : true;
            const experienceFilter = filterBy === 'base_experience' && pokemon.base_experience === maxExperience;
            const heightFilter = filterBy === 'height' && pokemon.height === maxHeight;
            const weightFilter = filterBy === 'weight' && pokemon.weight === maxWeight;

            return nameMatch && (!filterBy || experienceFilter || heightFilter || weightFilter);
        });

    return (
        <div>
            <h1>Pokémon Table</h1>
            <FormControl
                type="text"
                placeholder="Search by name"
                value={searchTerm}
                onChange={handleSearchChange}
            />
            <FormControl as="select" value={filterBy} onChange={handleFilterChange}>
                <option value="">Filter by...</option>
                <option value="base_experience">Base Experience</option>
                <option value="height">Height</option>
                <option value="weight">Weight</option>
            </FormControl>
            <Table striped bordered hover>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Base Experience</th>
                        <th>Height</th>
                        <th>Weight</th>
                        <th>Image</th>
                    </tr>
                </thead>
                <tbody>
                    {filteredPokemonData.map((pokemon) => (
                        <tr key={pokemon.id}>
                            <td>{pokemon.id}</td>
                            <td>{pokemon.name}</td>
                            <td>{pokemon.base_experience}</td>
                            <td>{pokemon.height}</td>
                            <td>{pokemon.weight}</td>
                            <td>
                                <PokemonImage imageUrl={pokemon.image_url} altText={pokemon.name} />
                            </td>
                        </tr>
                    ))}
                </tbody>
            </Table>
            <Pagination>
                {Array.from({ length: Math.ceil(filteredPokemonData.length / ITEMS_PER_PAGE) }).map((_, index) => (
                    <Pagination.Item
                        key={index}
                        active={index + 1 === currentPage}
                        onClick={() => handlePageChange(index + 1)}
                    >
                        {index + 1}
                    </Pagination.Item>
                ))}
            </Pagination>
        </div>
    );
};

export default PokemonTable;
