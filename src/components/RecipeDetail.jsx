function RecipeDetail({ recipe, onClose}) {
  return (
    <section className="border-t border-stone-200 bg-white"> 
        <div className="mx-auto max-w-3xl px-6 py-16">
            <button onClick={onClose} className="mb-8 text-sm font-semibold text-orange-600 hover:text-orange-700">
            ← Back to recipes
            </button>
            <div className="text-5xl">
                {recipe.emoji}
            </div>
            <h2 className="mt-4 text-4xl font-bold tracking-tight text-slate-950">
                {recipe.name}
            </h2>
            <p className="mt-4 text-lg leading-8 text-slate-600">
                {recipe.description}
            </p>
            <div className="mt-6 flex gap-4 text-sm text-slate-500">
                <span>{recipe.cookTime} min</span>
                <span>•</span>
                <span>{recipe.difficulty}</span>
            </div>
            <div className="mt-10">
                <h3 className="text-2xl font-bold text-slate-950">
                    Ingredients
                </h3>

                <ul className="mt-4 space-y-2 text-slate-700">
                    {recipe.ingredients.map((ingredient) => (
                    <li key={ingredient}>
                        • {ingredient}
                    </li>
                    ))}
                </ul>
            </div>
            <div className="mt-10">
                <h3 className="text-2xl font-bold text-slate-950">
                    Instructions
                </h3>

                <ol className="mt-4 space-y-4 text-slate-700">
                    {recipe.instructions.map((instruction, index) => (
                    <li key={instruction}>
                        <span className="font-semibold">
                        {index + 1}.
                        </span>{" "}
                        {instruction}
                    </li>
                    ))}
                </ol>
            </div>
        </div>
    </section>
  );
}

export default RecipeDetail;