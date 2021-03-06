pub mod hex_coordinates;
//pub mod demo;

use std::collections::HashMap;
use serde::{Serialize, Deserialize};
use hex_coordinates::{HexCoord, Tile, Edge, Corner};

#[derive(Debug, Clone, Eq, PartialEq, Serialize, Deserialize)]
pub struct HexGrid<T, E, C> {
    pub tiles: HashMap<Tile, T>,
    pub edges: HashMap<Edge, E>,
    pub corners: HashMap<Corner, C>
}

impl<T, E, C> HexGrid<T, E, C> {
    pub fn new() -> Self {
        HexGrid {
            tiles: HashMap::new(),
            edges: HashMap::new(),
            corners: HashMap::new()
        }
    }

    pub fn get_tile_neighbors<CoordType: HexCoord>(&self, coords: &CoordType) -> Vec<(Tile, &T)> {
        coords.get_tile_neighbors().into_iter()
            .map(|c| self.tiles.get(&c).map(|data| (c, data)))
            .flatten()
            .collect()
    }

    pub fn get_corner_neighbors<CoordType: HexCoord>(&self, coords: &CoordType) -> Vec<(Corner, &C)> {
        coords.get_corner_neighbors().into_iter()
            .map(|c| self.corners.get(&c).map(|data| (c, data)))
            .flatten()
            .collect()
    }

    pub fn get_edge_neighbors<CoordType: HexCoord>(&self, coords: &CoordType) -> Vec<(Edge, &E)> {
        coords.get_edge_neighbors().into_iter()
            .map(|c| self.edges.get(&c).map(|data| (c, data)))
            .flatten()
            .collect()
    }
}