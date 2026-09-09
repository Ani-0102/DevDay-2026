import { createContext, useContext, useEffect, useState } from "react";
import {
  getFavoritesRequest,
  getUserId,
  toggleFavoriteRequest,
} from "../services/api";

const FavoritesContext = createContext(null);

export function FavoritesProvider({ children }) {
  const [favorites, setFavorites] = useState([]);

  useEffect(() => {
    let cancelled = false;

    async function loadFavorites() {
      try {
        const userId = getUserId();
        const savedFavorites = await getFavoritesRequest(userId);

        if (!cancelled) {
          setFavorites(savedFavorites);
        }
      } catch (error) {
        console.error("Could not load favorites:", error);
      }
    }

    loadFavorites();

    return () => {
      cancelled = true;
    };
  }, []);

  async function toggleFavorite(recipe) {
    try {
        const userId = getUserId();

        const updatedFavorites =
        await toggleFavoriteRequest(userId, recipe);

        setFavorites(updatedFavorites);
    } catch (error) {
        console.error("Could not update favorites:", error);
    }
  }

  return (
    <FavoritesContext.Provider value={{ favorites, setFavorites, toggleFavorite }}>
      {children}
    </FavoritesContext.Provider>
  );
}

export function useFavorites() {
  return useContext(FavoritesContext);
}
