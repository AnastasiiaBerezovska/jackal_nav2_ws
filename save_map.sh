#!/bin/bash

# Assisting with map saving | making sure it no longer gets deleted
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

TEMP_MAP="/home/robot/jackal_nav2_ws/maps/lio_sam_temp/GlobalMap.pcd"
SAVE_DIR="/home/robot/jackal_nav2_ws/maps/lio_sam_3d"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

if [ ! -f "$TEMP_MAP" ]; then
    echo -e "${RED} No map found in temp directory!${NC}"
    exit 1
fi

SIZE=$(du -h "$TEMP_MAP" | cut -f1)
echo "Map size: $SIZE"

read -p "Save this map? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    cp "$TEMP_MAP" "$SAVE_DIR/GlobalMap_${TIMESTAMP}.pcd"
    chmod 444 "$SAVE_DIR/GlobalMap_${TIMESTAMP}.pcd"
    ln -sf "$SAVE_DIR/GlobalMap_${TIMESTAMP}.pcd" "$SAVE_DIR/GlobalMap.pcd"
    
    echo -e "${GREEN} Map saved as: GlobalMap_${TIMESTAMP}.pcd${NC}"
    echo -e "${GREEN} Symlink created: GlobalMap.pcd → GlobalMap_${TIMESTAMP}.pcd${NC}"
    
    # Clean temp
    read -p "Clean temp directory? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf /home/robot/jackal_nav2_ws/maps/lio_sam_temp/*
        echo -e "${GREEN} Temp directory cleaned${NC}"
    fi
else
    echo "Map not saved"
fi