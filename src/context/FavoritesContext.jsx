import { createContext, useContext, useState } from "react";
import { getUserId, toggleFavoriteRequest,} from "../services/api";

const FavoritesContext = createContext(null);

export function FavoritesProvider({ children }) {
  const [favorites, setFavorites] = useState([]);

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