class Restaurant {
  constructor(name, lunchRegex, imageUrlRegex, time) {
    this.name = name;
    this.lunchRegex = lunchRegex;
    this.imageUrlRegex = imageUrlRegex;
    this.time = time;
  }

  toDict() {
    return {
      name: this.name,
      lunchRegex: this.lunchRegex,
      imageUrlRegex: this.imageUrlRegex,
      time: this.time,
    };
  }
}
