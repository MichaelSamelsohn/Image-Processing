import numpy as np

def addNoise(self, noise_typ):
    # TODO: Finish implementation.
    if noise_typ == "gauss":
        row, col, ch = self.image.shape
        mean = 0
        var = 0.1
        sigma = var ** 0.5
        gauss = np.random.normal(mean, sigma, (row, col, ch))
        gauss = gauss.reshape(row, col, ch)
        self.image = self.image + gauss
    elif noise_typ == "s&p":
        s_vs_p = 0.5
        amount = 0.004
        out = np.copy(self.image)
        # Salt mode
        num_salt = np.ceil(amount * self.image.size * s_vs_p)
        coords = [np.random.randint(0, i - 1, int(num_salt))
                  for i in self.image.shape]
        out[coords] = 255

        # Pepper mode
        num_pepper = np.ceil(amount * self.image.size * (1. - s_vs_p))
        coords = [np.random.randint(0, i - 1, int(num_pepper))
                  for i in self.image.shape]
        out[coords] = 0
        self.image = out

    elif noise_typ == "poisson":
        vals = len(np.unique(self.image))
        vals = 2 ** np.ceil(np.log2(vals))
        noisy = np.random.poisson(self.image * vals) / float(vals)
        return noisy

    elif noise_typ == "speckle":
        row, col, ch = self.image.shape
        gauss = np.random.randn(row, col, ch)
        gauss = gauss.reshape(row, col, ch)
        noisy = self.image + self.image * gauss
        return noisy