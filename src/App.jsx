import Navbar from "./components/Navbar";
import Hero from "./components/Hero";
import RecipeList from "./components/RecipeList";
import RecipeDetail from "./components/RecipeDetail";
import { useState } from "react";
import VoiceAssistant from "./components/VoiceAssistant";


import { recipes } from "./data/recipes";

function App() {
  const [selectedRecipe, setSelectedRecipe] = useState(null);
  const [search, setSearch] = useState("");
  const filteredRecipes = recipes.filter((recipe) =>
    recipe.name.toLowerCase().includes(search.toLowerCase())
  );
  return (
    <div className="min-h-screen bg-stone-50 text-slate-900">
      <Navbar />
      <main>
        <Hero />
        {selectedRecipe ? (<RecipeDetail recipe={selectedRecipe} onClose={() => setSelectedRecipe(null)} /> ) : (
          <RecipeList
            recipes={filteredRecipes}
            onSelectRecipe={setSelectedRecipe}
            search={search}
            onSearchChange={setSearch}
          />
        )}
        <VoiceAssistant />
      </main>

      <footer className="border-t border-stone-200 bg-white">
        <div className="mx-auto max-w-5xl px-6 py-8 text-center text-sm text-slate-500">
          Built at HackUTD DevDay 2026
        </div>
      </footer>
    </div>
  );
}

export default App;
