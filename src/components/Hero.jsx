function Hero() {
  return (
    <div className="mx-auto max-w-5xl px-6 py-20">
      <p className="text-sm font-semibold uppercase tracking-[0.15em] text-orange-600">
        HackUTD DevDay 2026
      </p>
      <h1 className="mt-4 text-5xl font-bold tracking-tight text-slate-950">
        Find your next favorite recipe.
      </h1>
      <p className="mt-6 text-lg leading-8 text-slate-600">
        Browse our collection of delicious recipes and discover new flavors to try in your kitchen.
      </p>
      <a href="#recipes" className="mt-8 inline-block rounded-lg bg-slate-950 px-5 py-3 text-sm font-semibold text-white hover:bg-slate-800"
      >
        Browse recipes
      </a>
    </div>
  );
}

export default Hero;
