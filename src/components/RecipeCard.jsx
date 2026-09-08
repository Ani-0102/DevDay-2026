import { useFavorites } from "../context/FavoritesContext";

function RecipeCard({ recipe, onSelectRecipe}) {
  const { favorites, toggleFavorite } = useFavorites();
  const isFavorite = favorites.some((favorite) => favorite.id === recipe.id);
  return (
    <article className="grid gap-4 border-b border-stone-200 py-7 md:grid-cols-[64px_1fr_auto] md:items-center">
      <div className="flex h-14 w-14 items-center justify-center rounded-xl bg-white text-3xl shadow-sm ring-1 ring-stone-200">
        {recipe.emoji}
      </div>
      <div> 
        <h3 className="text-lg font-semibold text-slate-950"> 
          {recipe.name}
        </h3>
        <p className="text-lg font-semibold text-slate-950">
          {recipe.description}
        </p>
      </div>
      <div className="text-sm text-slate-500 md:text-right">
        <span>{recipe.cookTime} min</span>
        <span> · {recipe.difficulty}</span>
      </div>
      <button onClick={() => onSelectRecipe(recipe)} 
      className="rounded-lg bg-slate-950 px-4 py-2 text-sm font-semibold text-white hover:bg-slate-800">
        View Recipe
      </button>
      <button onClick={() => toggleFavorite(recipe)} className="text-2xl transition hover:scale-110" aria-label={isFavorite ? "Remove from favorites" : "Add to favorites"}
      >
        {isFavorite ? "♥" : "♡"}
      </button>
    </article>
  );
}

export default RecipeCard;