import torch
import torch.nn as nn


class SpatialTemporal(nn.Module):
    """Generates feature vectors Vsp and Vtp for each particular cell"""

    spatial_emb_dims = [
        ('G_X', 256, 5),
        ('G_Y', 256, 5)
    ]

    temporal_emb_dims = [
        ('day_bin', 7, 3),
        ('hour_bin', 24, 4),
        ('time_bin', 287, 5)
    ]

    def __init__(self):
        super(SpatialTemporal, self).__init__()
        self.build()

    def build(self):
        for name, dim_in, dim_out in (SpatialTemporal.spatial_emb_dims + SpatialTemporal.temporal_emb_dims):
            self.add_module(name + '_em', nn.Embedding(dim_in, dim_out))

    def forward(self, stats, temporal, spatial):

        V_tp = []
        for name, dim_in, dim_out in SpatialTemporal.temporal_emb_dims:
            embed = getattr(self, name + '_em')
            temporal_t = temporal[name].view(-1, 1)
            temporal_t = torch.squeeze(embed(temporal_t))
            V_tp.append(temporal_t)

        V_sp = []
        for name, dim_in, dim_out in SpatialTemporal.spatial_emb_dims:
            embed = getattr(self, name + '_em')
            spatial_t = spatial[name].view(-1, 1)
            spatial_t = torch.squeeze(embed(spatial_t))
            V_sp.append(spatial_t)

        V_tp = torch.cat(V_tp, dim=1) # length is batch_size * len(max_batch_path)
        V_sp = torch.cat(V_sp, dim=1) # length is batch_size * len(max_batch_path)
        return V_sp, V_tp
