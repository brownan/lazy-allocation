/**
 * Calculates how much to contribute to each fund given a fixed contribution amount
 * 
 * @param {current_values} A column of current values
 * @param {target_allocs} A column of percentages
 * @param {contribution} The amount to contribute
 * @return A column of delta values, how much to contribute to each fund
 * @customfunction
 */
function LAZYALLOC(current_values, target_allocs, C) {
  // first, flatten the arrays
  current_values = current_values.map(item => item[0]).filter(item => item !== '');
  target_allocs = target_allocs.map(item => item[0]);

  // combine into a list of asset objects
  let assets = current_values.map((a, i) => ({
    a: a,
    d: target_allocs[i],
    i: i
  }));

  // calculate the target value and fractional deviation of each
  let T = assets.map(a => a.a).reduce((x, y) => x + y) + C;
  assets.forEach(asset => {
    asset.t = T * asset.d || 0.001;
    asset.f = asset.a / asset.t;
  })

  // sort the assets
  assets.sort((a, b) => a.f - b.f);
  if (C < 0) {
    assets.reverse();
  }

  let step = 0;
  let r = 0;
  let prev_TC = 0;
  let this_f;

  while (true) {
    this_f = assets[step].f;
    r += assets[step].t;

    if ((step + 1) === assets.length) {
      break;
    }

    let next_f = assets[step+1].f;
    let TC = prev_TC + r * (next_f - this_f);

    if (Math.abs(TC) >= Math.abs(C)) {
      break;
    }

    step += 1;
    prev_TC = TC;
  }

  let f_f = this_f + (C - prev_TC) / r;

  assets.forEach((asset, i) => {
    if (i <= step) {
      asset.delta = asset.t * (f_f - asset.f);
    } else {
      asset.delta = 0;
    }
  })
  assets.sort((x, y) => x.i - y.i);

  return assets.map(asset => [asset.delta]);
}
