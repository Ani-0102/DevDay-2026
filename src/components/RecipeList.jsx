import RecipeCard from "./RecipeCard";
import SearchBar from "./SearchBar";

function RecipeList({ recipes, onSelectRecipe, search, onSearchChange,}) {
  return (
    
    <div id="recipes" className="mx-auto max-w-5xl px-6 py-16"> 
      <p className="text-sm font-semibold uppercase tracking-[0.15em] text-orange-600"
      > Recipes</p>
      <h2 className="mt-2 text-3xl font-bold tracking-tight text-slate-950">
        Starter recipes
      </h2>
      <p className="mt-3 max-w-2xl text-slate-600">
        Browse a few recipes to get started.
      </p>
      <SearchBar
        search={search}
        onSearchChange={onSearchChange}
      />
      {recipes.map((recipe) => (
        <RecipeCard key={recipe.id} recipe={recipe} onSelectRecipe={onSelectRecipe}/>
      ))}
    </div>
  );
}

export default RecipeList;