function Navbar() {
  return (
    <nav className="border-b border-stone-200 bg-white">
      <div className="mx-auto flex max-w-5xl items-center justify-between px-6 py-4">
        <a
          href="#top"
          className="text-xl font-bold tracking-tight text-slate-950"
        >
          DevDay Recipes
        </a>

        <div className="flex items-center gap-6 text-sm font-medium text-slate-600">
          <a
            href="#recipes"
            className="hover:text-orange-600"
          >
            Recipes
          </a>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;