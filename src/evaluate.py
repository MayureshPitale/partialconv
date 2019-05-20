import torch
from torchvision.utils import make_grid
from torchvision.utils import save_image


def evaluate(model, dataset, device, filename, experiment=None):
    image, mask, gt = zip(*[dataset[i] for i in range(8)])
    image = torch.stack(image)
    mask = torch.stack(mask)
    gt = torch.stack(gt)
    with torch.no_grad():
        output, _ = model(image.to(device), mask.to(device))
    output = output.to(torch.device('cpu'))
    output_comp = mask * image + (1 - mask) * output

    grid = make_grid(torch.cat(image, mask, output, output_comp, gt), dim=0)
    save_image(grid, filename)
    if experiment:
        experiment.log_image(grid, filename)