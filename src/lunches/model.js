class Restaurant {
  constructor(name, url, lunchRegex, imageUrlRegex, time) {
    this.name = name;
    this.url = url;
    this.lunchRegex = lunchRegex;
    this.imageUrlRegex = imageUrlRegex;
    this.time = time;
  }

  toDict() {
    return {
      name: this.name,
      url: this.url,
      requirements: {
        lunchRegex: this.lunchRegex,
        imageUrlRegex: this.imageUrlRegex,
        time: this.time,
      },
    };
  }
}

export {Restaurant};