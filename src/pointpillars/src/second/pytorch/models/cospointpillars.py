"""
PointPillars fork from SECOND.
Code written by Alex Lang and Oscar Beijbom, 2018.
Licensed under MIT License [see LICENSE].
"""

import torch
from torch import nn
from torch.nn import functional as F

from second.pytorch.utils import get_paddings_indicator
from torchplus.nn import Empty
from torchplus.tools import change_default_args


class PFNLayer(nn.Module):
    def __init__(self,
                 in_channels,
                 out_channels,
                 use_norm=True,
                 last_layer=False,cos_layer=False):
        """
        Pillar Feature Net Layer.
        The Pillar Feature Net could be composed of a series of these layers, but the PointPillars paper results only
        used a single PFNLayer. This layer performs a similar role as second.pytorch.voxelnet.VFELayer.
        :param in_channels: <int>. Number of input channels.
        :param out_channels: <int>. Number of output channels.
        :param use_norm: <bool>. Whether to include BatchNorm.
        :param last_layer: <bool>. If last_layer, there is no concatenation of features.
        """

        super().__init__()
        self.name = 'PFNcosLayer'
        self.last_vfe = last_layer
        self.cos = cos_layer
        if not self.last_vfe:
        
            out_channels = out_channels // 2


        self.units = out_channels

        if use_norm:
            BatchNorm1d = change_default_args(eps=1e-3, momentum=0.01)(nn.BatchNorm1d)
            Linear = change_default_args(bias=False)(nn.Linear)
        else:
            BatchNorm1d = Empty
            Linear = change_default_args(bias=True)(nn.Linear)

        self.linear = Linear(in_channels, self.units)
        self.norm = BatchNorm1d(self.units)

    def forward(self, inputs):

        print(inputs.size())

        x = self.linear(inputs)
        
        x = self.norm(x.permute(0, 2, 1).contiguous()).permute(0, 2, 1).contiguous()
        x = F.relu(x)

        x_max = torch.max(x, dim=1, keepdim=True)[0]

        if self.cos ==False:

            if self.last_vfe:
                return x_max
            else:
                x_repeat = x_max.repeat(1, inputs.shape[1], 1)
                x_concatenated = torch.cat([x, x_repeat], dim=2)
                return x_concatenated
        else:
            if self.last_vfe:
                return x
            
            else:
                x_repeat = x_max.repeat(1, inputs.shape[1], 1)
                x_concatenated = torch.cat([x, x_repeat], dim=2)
                return x_concatenated
            
class cosPillarFeatureNet(nn.Module):
    def __init__(self,
                 num_input_features=4,
                 use_norm=True,
                 num_filters=(64,),
                 with_distance=False,
                 voxel_size=(0.2, 0.2, 4),
                 pc_range=(0, -40, -3, 70.4, 40, 1)):
        """
        Pillar Feature Net.
        The network prepares the pillar features and performs forward pass through PFNLayers. This net performs a
        similar role to SECOND's second.pytorch.voxelnet.VoxelFeatureExtractor.
        :param num_input_features: <int>. Number of input features, either x, y, z or x, y, z, r.
        :param use_norm: <bool>. Whether to include BatchNorm.
        :param num_filters: (<int>: N). Number of features in each of the N PFNLayers.
        :param with_distance: <bool>. Whether to include Euclidean distance to points.
        :param voxel_size: (<float>: 3). Size of voxels, only utilize x and y size.
        :param pc_range: (<float>: 6). Point cloud range, only utilize x and y min.
        """

        super().__init__()
        self.name = 'cosPillarFeatureNet'
        assert len(num_filters) > 0
        num_input_features += 5
        if with_distance:
            num_input_features += 1
        self._with_distance = with_distance



        

        # Create PillarFeatureNet layers
        num_filters = [num_input_features] + list(num_filters)
        
        pfn_layers = []
        theta_layers = []
        # for i in range(len(num_filters) - 1):
        #     in_filters = num_filters[i]
        #     out_filters = num_filters[i + 1]
        #     if i < len(num_filters) - 2:
        #         last_layer = False
        #     else:
        #         last_layer = True
        #     pfn_layers.append(PFNLayer(in_filters, out_filters, use_norm, last_layer=last_layer))
        pfn_layers.append(PFNLayer(9, 64, use_norm, last_layer=True))
        self.pfn_layers = nn.ModuleList(pfn_layers)


        # theta_layers.append(PFNLayer(8, 64,use_norm, last_layer=False,cos_layer =True))
        # theta_layers.append(PFNLayer(64, 16, use_norm, last_layer=False,cos_layer =True))
        # theta_layers.append(PFNLayer(16, 1, use_norm, last_layer=True,cos_layer =True))
        theta_layers.append(PFNLayer(6, 64,use_norm, last_layer=False,cos_layer =True))
        theta_layers.append(PFNLayer(64, 32, use_norm, last_layer=False,cos_layer =True))
        theta_layers.append(PFNLayer(32, 8, use_norm, last_layer=False,cos_layer =True))
        theta_layers.append(PFNLayer(8, 1, use_norm, last_layer=True,cos_layer =True))
        self.theta_layers = nn.ModuleList(theta_layers)

        # Need pillar (voxel) size and x/y offset in order to calculate pillar offset
        self.vx = voxel_size[0]
        self.vy = voxel_size[1]
        self.x_offset = self.vx / 2 + pc_range[0]
        self.y_offset = self.vy / 2 + pc_range[1]

    def forward(self, features, num_voxels, coors):
#only use avobe >-1.6

        #features_mask =torch.where((features>-1.6),torch.ones(features.shape[0],features.shape[1],features.shape[2],device ="cuda:0"),0.1*torch.ones(features.shape[0],features.shape[1],features.shape[2],device ="cuda:0"))
        

        # Find distance of x, y, and z from cluster center
        points_mean = features[:, :, :3].sum(dim=1, keepdim=True) / num_voxels.type_as(features).view(-1, 1, 1)
        f_cluster = features[:, :, :3] - points_mean

        # Find distance of x, y, and z from pillar center
        f_center = torch.zeros_like(features[:, :, :2])
        f_center[:, :, 0] = features[:, :, 0] - (coors[:, 3].float().unsqueeze(1) * self.vx + self.x_offset)
        f_center[:, :, 1] = features[:, :, 1] - (coors[:, 2].float().unsqueeze(1) * self.vy + self.y_offset)

        # Combine together feature decorations
        features_ls = [features[:, :, :3], f_cluster, f_center]
        coss = features[:,:,3]
        if self._with_distance:
            points_dist = torch.norm(features[:, :, :3], 2, 2, keepdim=True)
            features_ls.append(points_dist)
        features = torch.cat(features_ls, dim=-1)


        theta_features_ls = [features[:, :, :3], f_cluster]
        
        theta_features = torch.cat(theta_features_ls, dim=-1)

        #print(features)

        # The feature decorations were calculated without regard to whether pillar was empty. Need to ensure that
        # empty pillars remain set to zeros.
        voxel_count = features.shape[1]
        mask = get_paddings_indicator(num_voxels, voxel_count, axis=0)
        mask = torch.unsqueeze(mask, -1).type_as(features)
        features *= mask

        #print(features)

        # Forward pass through PFNLayers


        target_thetas = torch.reshape(coss,(-1,50,1))
        #features_mask_z = torch.reshape(features_mask[:,:,2],(-1,25,1))
        #print(features_mask_z)

        voxel_count = target_thetas.shape[1]
        mask = get_paddings_indicator(num_voxels, voxel_count, axis=0)
        mask = torch.unsqueeze(mask, -1).type_as(target_thetas)
        target_thetas *= mask

        #print(target_thetas.size())
        

        
        #print(theta_features.size())
        for theta in self.theta_layers:
            theta_features = theta(theta_features)

        voxel_count = target_thetas.shape[1]
        mask = get_paddings_indicator(num_voxels, voxel_count, axis=0)
        mask = torch.unsqueeze(mask, -1).type_as(theta_features)
        theta_features *= mask


        features_LS = [theta_features,features]
        features = torch.cat(features_LS, dim=-1)
        #print(features.size())
        for pfn in self.pfn_layers:
            #print(features.size())
            features = pfn(features)
        

        criterion = nn.MSELoss()

        theta_loss = criterion(theta_features, target_thetas)

        #print(num_voxels)
        #print(features_mask_z.sum())

        theta_loss = theta_loss/(num_voxels.sum() +0.001) *50*features.shape[0]

        print(theta_loss)

        return features.squeeze(), theta_loss*0.5











































class cosPillarFeatureNet_mask(nn.Module):
    def __init__(self,
                 num_input_features=4,
                 use_norm=True,
                 num_filters=(64,),
                 with_distance=False,
                 voxel_size=(0.2, 0.2, 4),
                 pc_range=(0, -40, -3, 70.4, 40, 1)):
        """
        Pillar Feature Net.
        The network prepares the pillar features and performs forward pass through PFNLayers. This net performs a
        similar role to SECOND's second.pytorch.voxelnet.VoxelFeatureExtractor.
        :param num_input_features: <int>. Number of input features, either x, y, z or x, y, z, r.
        :param use_norm: <bool>. Whether to include BatchNorm.
        :param num_filters: (<int>: N). Number of features in each of the N PFNLayers.
        :param with_distance: <bool>. Whether to include Euclidean distance to points.
        :param voxel_size: (<float>: 3). Size of voxels, only utilize x and y size.
        :param pc_range: (<float>: 6). Point cloud range, only utilize x and y min.
        """

        super().__init__()
        self.name = 'cosPillarFeatureNet_mask'
        assert len(num_filters) > 0
        num_input_features += 5
        if with_distance:
            num_input_features += 1
        self._with_distance = with_distance



        

        # Create PillarFeatureNet layers
        num_filters = [num_input_features] + list(num_filters)
        
        pfn_layers = []
        theta_layers = []
        # for i in range(len(num_filters) - 1):
        #     in_filters = num_filters[i]
        #     out_filters = num_filters[i + 1]
        #     if i < len(num_filters) - 2:
        #         last_layer = False
        #     else:
        #         last_layer = True
        #     pfn_layers.append(PFNLayer(in_filters, out_filters, use_norm, last_layer=last_layer))
        pfn_layers.append(PFNLayer(9, 64, use_norm, last_layer=True))
        self.pfn_layers = nn.ModuleList(pfn_layers)


        theta_layers.append(PFNLayer(8, 64,use_norm, last_layer=False,cos_layer =True))
        theta_layers.append(PFNLayer(64, 16, use_norm, last_layer=False,cos_layer =True))
        #theta_layers.append(PFNLayer(32, 8, use_norm, last_layer=False,cos_layer =True))
        #theta_layers.append(PFNLayer(64, 16, use_norm, last_layer=False,cos_layer =True))
        theta_layers.append(PFNLayer(16, 1, use_norm, last_layer=True,cos_layer =True))
        self.theta_layers = nn.ModuleList(theta_layers)

        # Need pillar (voxel) size and x/y offset in order to calculate pillar offset
        self.vx = voxel_size[0]
        self.vy = voxel_size[1]
        self.x_offset = self.vx / 2 + pc_range[0]
        self.y_offset = self.vy / 2 + pc_range[1]

    def forward(self, features, num_voxels, coors):
#only use avobe >-1.6

        #features_mask =torch.where((features>-1.6),torch.ones(features.shape[0],features.shape[1],features.shape[2],device ="cuda:0"),torch.zeros(features.shape[0],features.shape[1],features.shape[2],device ="cuda:0"))
        

        # Find distance of x, y, and z from cluster center
        points_mean = features[:, :, :3].sum(dim=1, keepdim=True) / num_voxels.type_as(features).view(-1, 1, 1)
        f_cluster = features[:, :, :3] - points_mean

        # Find distance of x, y, and z from pillar center
        f_center = torch.zeros_like(features[:, :, :2])
        f_center[:, :, 0] = features[:, :, 0] - (coors[:, 3].float().unsqueeze(1) * self.vx + self.x_offset)
        f_center[:, :, 1] = features[:, :, 1] - (coors[:, 2].float().unsqueeze(1) * self.vy + self.y_offset)

        # Combine together feature decorations
        features_ls = [features[:, :, :3], f_cluster, f_center]
        coss = torch.acos(features[:,:,3])
        if self._with_distance:
            points_dist = torch.norm(features[:, :, :3], 2, 2, keepdim=True)
            features_ls.append(points_dist)
        features = torch.cat(features_ls, dim=-1)


        theta_features_ls = [features[:, :, :3], f_cluster]
        coss = torch.acos(features[:,:,3])
        if self._with_distance:
            points_dist = torch.norm(features[:, :, :3], 2, 2, keepdim=True)
            theta_features_ls.append(points_dist)
        theta_features = torch.cat(theta_features_ls, dim=-1)

        #print(features)

        # The feature decorations were calculated without regard to whether pillar was empty. Need to ensure that
        # empty pillars remain set to zeros.
        voxel_count = features.shape[1]
        mask = get_paddings_indicator(num_voxels, voxel_count, axis=0)
        mask = torch.unsqueeze(mask, -1).type_as(features)
        features *= mask

        #print(features)

        # Forward pass through PFNLayers
        target_thetas = torch.reshape(coss,(-1,50,1))
        #features_mask_z = torch.reshape(features_mask[:,:,2],(-1,25,1))
        #print(features_mask_z)

        voxel_count = target_thetas.shape[1]
        mask = get_paddings_indicator(num_voxels, voxel_count, axis=0)
        mask = torch.unsqueeze(mask, -1).type_as(target_thetas)
        target_thetas *= mask

        #print(target_thetas.size())
        
        #print(theta_features.size())
        for theta in self.theta_layers:
            theta_features = theta(theta_features)

        voxel_count = target_thetas.shape[1]
        mask = get_paddings_indicator(num_voxels, voxel_count, axis=0)
        mask = torch.unsqueeze(mask, -1).type_as(theta_features)
        theta_features *= mask


        features_LS = [theta_features,features]
        features = torch.cat(features_LS, dim=-1)
        #print(features.size())
        for pfn in self.pfn_layers:
            #print(features.size())
            features = pfn(features)
        

        criterion = nn.MSELoss()

        theta_loss = criterion(theta_features, target_thetas)

        #print(num_voxels)
        #print(features_mask_z.sum())

        theta_loss = theta_loss/(num_voxels.sum() +0.001) *50*features.shape[0]

        print(theta_loss)

        return features.squeeze(), theta_loss * 1.0


class PointPillarsScatter(nn.Module):
    def __init__(self,
                 output_shape,
                 num_input_features=64):
        """
        Point Pillar's Scatter.
        Converts learned features from dense tensor to sparse pseudo image. This replaces SECOND's
        second.pytorch.voxelnet.SparseMiddleExtractor.
        :param output_shape: ([int]: 4). Required output shape of features.
        :param num_input_features: <int>. Number of input features.
        """

        super().__init__()
        self.name = 'PointPillarsScatter'
        self.output_shape = output_shape
        self.ny = output_shape[2]
        self.nx = output_shape[3]
        self.nchannels = num_input_features

    def forward(self, voxel_features, coords, batch_size):

        # batch_canvas will be the final output.
        batch_canvas = []
        for batch_itt in range(batch_size):
            # Create the canvas for this sample
            canvas = torch.zeros(self.nchannels, self.nx * self.ny, dtype=voxel_features.dtype,
                                 device=voxel_features.device)

            # Only include non-empty pillars
            batch_mask = coords[:, 0] == batch_itt
            this_coords = coords[batch_mask, :]
            indices = this_coords[:, 2] * self.nx + this_coords[:, 3]
            indices = indices.type(torch.long)
            voxels = voxel_features[batch_mask, :]
            voxels = voxels.t()

            # Now scatter the blob back to the canvas.
            canvas[:, indices] = voxels

            # Append to a list for later stacking.
            batch_canvas.append(canvas)

        # Stack to 3-dim tensor (batch-size, nchannels, nrows*ncols)
        batch_canvas = torch.stack(batch_canvas, 0)

        # Undo the column stacking to final 4-dim tensor
        batch_canvas = batch_canvas.view(batch_size, self.nchannels, self.ny, self.nx)

        return batch_canvas
