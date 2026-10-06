#!/usr/bin/env python3
"""Export all portfolio data to portfolio.txt for chatbot knowledge base."""

import json
import sys
import os

# Add current directory to path to import from main
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import get_projects, get_records, get_attributes


def export_portfolio_txt(output_path: str = "portfolio.txt"):
    """Export all portfolio data to a structured text file."""
    
    projects_data = get_projects()
    records_data = get_records()
    attributes_data = get_attributes()
    
    lines = []
    lines.append("=" * 80)
    lines.append("UJJWAL PORTFOLIO - COMPLETE KNOWLEDGE BASE")
    lines.append("=" * 80)
    lines.append("")
    
    # ========== PROJECTS ==========
    lines.append("SECTION: PROJECTS")
    lines.append("-" * 80)
    lines.append(f"Formation: {projects_data['formation']}")
    lines.append(f"Total Shipped: {projects_data['total_shipped']}")
    lines.append(f"Active Builds: {projects_data['active_builds']}")
    lines.append("")
    
    for p in projects_data["projects"]:
        lines.append(f"PROJECT #{p['id']} - SQUAD NO. {p['squad_no']}")
        lines.append(f"  Title: {p['title']}")
        lines.append(f"  Position: {p['position']}")
        lines.append(f"  Category: {', '.join(p['category'])}")
        lines.append(f"  Subtitle: {p['subtitle']}")
        if 'fps' in p:
            lines.append(f"  FPS: {p['fps']}")
        if 'concurrency' in p:
            lines.append(f"  Concurrency: {p['concurrency']}")
        if 'tick_rate' in p:
            lines.append(f"  Tick Rate: {p['tick_rate']}")
        if 'uptime' in p:
            lines.append(f"  Uptime: {p['uptime']}")
        if 'status' in p:
            lines.append(f"  Status: {p['status']}")
        if 'scaling' in p:
            lines.append(f"  Scaling: {p['scaling']}")
        if 'components' in p:
            lines.append(f"  Components: {p['components']}")
        if 'feature' in p:
            lines.append(f"  Feature: {p['feature']}")
        if 'throughput' in p:
            lines.append(f"  Throughput: {p['throughput']}")
        if 'reliability' in p:
            lines.append(f"  Reliability: {p['reliability']}")
        lines.append(f"  Description: {p['description']}")
        lines.append(f"  Tags: {', '.join(p['tags'])}")
        lines.append("")
    
    # ========== EXPERIENCE ==========
    lines.append("SECTION: EXPERIENCE")
    lines.append("-" * 80)
    
    for exp in records_data["experience"]:
        lines.append(f"ROLE: {exp['role']}")
        lines.append(f"  Club/Org: {exp['club']}")
        lines.append(f"  Location: {exp['location']}")
        lines.append(f"  Period: {exp['period']} ({exp['status']})")
        lines.append(f"  Squad: {exp['squad']}")
        lines.append("  Highlights:")
        for h in exp["highlights"]:
            lines.append(f"    - {h}")
        lines.append("")
    
    # ========== EDUCATION ==========
    lines.append("SECTION: EDUCATION")
    lines.append("-" * 80)
    
    for edu in records_data["education"]:
        lines.append(f"DEGREE: {edu['degree']}")
        lines.append(f"  Academy: {edu['academy']}")
        lines.append(f"  Specialization: {edu['specialization']}")
        lines.append(f"  Period: {edu['period']}")
        lines.append(f"  Honours: {edu['honours']}")
        lines.append("")
    
    # ========== CERTIFICATIONS ==========
    lines.append("SECTION: CERTIFICATIONS")
    lines.append("-" * 80)
    
    for cert in records_data["certifications"]:
        lines.append(f"CERT: {cert['title']}")
        lines.append(f"  Year: {cert['year']}")
        lines.append(f"  Issuing Body: {cert['issuing_body']}")
        lines.append("")
    
    # ========== ATTRIBUTES ==========
    lines.append("SECTION: TACTICAL ATTRIBUTES")
    lines.append("-" * 80)
    
    # Player Identity
    pi = attributes_data["player_identity"]
    lines.append("PLAYER IDENTITY:")
    lines.append(f"  Name: {pi['name']}")
    lines.append(f"  Number: {pi['number']}")
    lines.append(f"  Role: {pi['role']}")
    lines.append(f"  Turf: {pi['turf']}")
    lines.append(f"  Overall Rating: {pi['ovr_rating']}")
    lines.append("")
    
    # FUT Attributes
    fa = attributes_data["fut_attributes"]
    lines.append("FUT ATTRIBUTES:")
    for attr, value in fa.items():
        lines.append(f"  {attr}: {value}")
    lines.append("")
    
    # Radar Scores
    rs = attributes_data["radar_scores"]
    lines.append("RADAR SCORES:")
    for skill, score in rs.items():
        lines.append(f"  {skill.replace('_', ' ').title()}: {score}")
    lines.append("")
    
    # Honours
    lines.append("HONOURS:")
    for h in attributes_data["honours"]:
        lines.append(f"  {h['title']} ({h['season']}) - {h['award']}")
    lines.append("")
    
    # ========== WRITE FILE ==========
    content = "\n".join(lines)
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"✅ Exported portfolio data to {output_path}")
    print(f"   Total characters: {len(content):,}")
    print(f"   Total lines: {len(lines):,}")
    
    return content


if __name__ == "__main__":
    export_portfolio_txt()