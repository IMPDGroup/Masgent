
import numpy as np
import pandas as pd
from tqdm import tqdm
from sklearn.discriminant_analysis import StandardScaler
import torch
import torch.nn as nn
from torch.nn.functional import mse_loss
from torch.utils.data import DataLoader, TensorDataset

# Conditional Variational Autoencoder (CVAE) for data augmentation
class CVAE(nn.Module):
    def __init__(self, x_dim, y_dim, latent_dim=8, hidden_dims=[64, 32, 16]):
        super().__init__()
        self.x_dim = x_dim
        self.y_dim = y_dim
        self.latent_dim = latent_dim

        # Encoder: takes both x and y as input
        encoder_layers = []
        input_dim = x_dim + y_dim
        for h in hidden_dims:
            encoder_layers += [nn.Linear(input_dim, h), nn.ReLU()]
            input_dim = h
        self.encoder = nn.Sequential(*encoder_layers)

        self.fc_mu = nn.Linear(input_dim, latent_dim)
        self.fc_logvar = nn.Linear(input_dim, latent_dim)

        # Decoder: takes latent + y
        decoder_layers = []
        input_dim = latent_dim + y_dim
        for h in reversed(hidden_dims):
            decoder_layers += [nn.Linear(input_dim, h), nn.ReLU()]
            input_dim = h
        decoder_layers += [nn.Linear(input_dim, x_dim)]
        self.decoder = nn.Sequential(*decoder_layers)

    def encode(self, x, y):
        xy = torch.cat([x, y], dim=1)
        h = self.encoder(xy)
        mu = self.fc_mu(h)
        logvar = self.fc_logvar(h)
        return mu, logvar

    def reparameterize(self, mu, logvar):
        std = torch.exp(0.5 * logvar)
        eps = torch.randn_like(std)
        return mu + eps * std

    def decode(self, z, y):
        zy = torch.cat([z, y], dim=1)
        x_recon = self.decoder(zy)
        return x_recon

    def forward(self, x, y):
        mu, logvar = self.encode(x, y)
        z = self.reparameterize(mu, logvar)
        x_recon = self.decode(z, y)
        return x_recon, mu, logvar

# CVAE Loss Function
def cvae_loss(x, x_recon, mu, logvar):
    recon = mse_loss(x_recon, x, reduction='mean')
    kl = -0.5 * torch.mean(1 + logvar - mu.pow(2) - logvar.exp())
    return recon + kl

# Training function for CVAE
def train_cvae(model, loader, epochs=500, lr=1e-3, patience=50):
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    best_loss = np.inf
    wait = 0

    for epoch in tqdm(range(epochs), desc="Training CVAE"):
        for x_batch, y_batch in loader:
            opt.zero_grad()
            x_recon, mu, logvar = model(x_batch, y_batch)
            loss = cvae_loss(x_batch, x_recon, mu, logvar)
            loss.backward()
            opt.step()

        # Early stopping
        if loss.item() < best_loss:
            best_loss = loss.item()
            wait = 0
        else:
            wait += 1
            if wait > patience:
                break

    return model

# Function to generate conditional samples using trained CVAE
def generate_conditional_samples(model, y_cond, num_samples=1):
    model.eval()
    latent_dim = model.latent_dim
    y_tensor = torch.tensor(y_cond, dtype=torch.float32)

    x_aug_list = []
    for _ in range(num_samples):
        z = torch.randn((1, latent_dim))
        x_aug = model.decode(z, y_tensor).detach().numpy().flatten()
        x_aug_list.append(x_aug)

    return np.array(x_aug_list)

# Main function to run CVAE-based data augmentation
def run_cvae_augmentation(input_df, output_df, num_aug=1000):
    x_dim = input_df.shape[1]
    y_dim = output_df.shape[1]

    # Scaling
    x_scaler = StandardScaler()
    y_scaler = StandardScaler()

    X = x_scaler.fit_transform(input_df.values)
    Y = y_scaler.fit_transform(output_df.values)

    dataset = TensorDataset(
        torch.tensor(X, dtype=torch.float32),
        torch.tensor(Y, dtype=torch.float32)
    )
    loader = DataLoader(dataset, batch_size=64, shuffle=True)

    cvae = CVAE(x_dim=x_dim, y_dim=y_dim, latent_dim=8, hidden_dims=[64, 32, 16])

    # Train CVAE
    cvae = train_cvae(cvae, loader)

    # Choose random outputs to condition on
    Y_choices = Y[np.random.choice(len(Y), size=num_aug, replace=True)]

    # Generate synthetic X conditioned on Y
    X_aug_std = []
    for y_cond in Y_choices:
        sample = generate_conditional_samples(cvae, y_cond.reshape(1, -1), num_samples=1)
        X_aug_std.append(sample[0])

    X_aug_std = np.array(X_aug_std)

    # Inverse transform to physical units
    X_aug = x_scaler.inverse_transform(X_aug_std)
    Y_aug = y_scaler.inverse_transform(Y_choices)

    x_aug_df = pd.DataFrame(X_aug, columns=input_df.columns)
    y_aug_df = pd.DataFrame(Y_aug, columns=output_df.columns)

    return x_aug_df, y_aug_df